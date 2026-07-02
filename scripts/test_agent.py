import os
import re
import sys
import json
from dotenv import load_dotenv

# Load env variables
load_dotenv()

# Add project root to sys.path
sys.path.append(os.getcwd())

from app.chat import chat

dir_path = 'data/sample_conversations/GenAI_SampleConversations'


def norm_url(url):
    return url.strip().rstrip('/').lower()


def parse_trace(path):
    content = open(path, 'r', encoding='utf-8').read()
    # Split content by Turn marker
    turns_raw = content.split('### Turn')[1:]
    
    parsed_turns = []
    
    for idx, t in enumerate(turns_raw):
        lines = t.strip().split('\n')
        turn_num = lines[0].strip()
        
        # Extract User message
        user_msg = ""
        user_idx = -1
        for i, line in enumerate(lines):
            if '**User**' in line:
                user_idx = i
                break
        if user_idx != -1:
            u_lines = []
            for l in lines[user_idx+1:]:
                if l.strip().startswith('>'):
                    u_lines.append(l.strip().lstrip('>').strip())
                elif l.strip() == "":
                    continue
                else:
                    break
            user_msg = " ".join(u_lines)
            
        # Extract Agent response
        agent_msg = ""
        agent_idx = -1
        for i, line in enumerate(lines):
            if '**Agent**' in line:
                agent_idx = i
                break
        if agent_idx != -1:
            a_lines = []
            for l in lines[agent_idx+1:]:
                if l.strip().startswith('_') or l.strip().startswith('|') or 'recommendations:' in l or 'end_of_conversation:' in l:
                    break
                a_lines.append(l.strip())
            agent_msg = " ".join([x for x in a_lines if x])
            
        # Extract Expected URLs from table rows
        urls = []
        for line in lines:
            if '|' in line and 'https://www.shl.com/products/product-catalog/view/' in line:
                match = re.search(r'https://www.shl.com/products/product-catalog/view/[a-zA-Z0-9\-\%]+/?', line)
                if match:
                    urls.append(match.group(0))
        
        # Extract Expected EOC
        eoc = False
        if "end_of_conversation`: **true**" in t.lower() or "end_of_conversation: true" in t.lower():
            eoc = True
            
        parsed_turns.append({
            "turn_num": turn_num,
            "user_msg": user_msg,
            "agent_msg": agent_msg,
            "expected_urls": urls,
            "expected_eoc": eoc
        })
        
    return parsed_turns


def run_evaluation():
    files = [f for f in sorted(os.listdir(dir_path)) if f.endswith('.md')]
    
    total_recall = 0.0
    total_turns_with_recs = 0
    total_turns_evaluated = 0
    schema_compliance_errors = 0
    eoc_matches = 0
    total_eoc_checks = 0
    
    print("=" * 60)
    print("RUNNING AGENT TRACE EVALUATION")
    print("=" * 60)
    
    for f_name in files:
        path = os.path.join(dir_path, f_name)
        turns = parse_trace(path)
        
        print(f"\nTrace: {f_name} ({len(turns)} turns)")
        print("-" * 40)
        
        history = []
        for turn in turns:
            # Append User message to history
            history.append({"role": "user", "content": turn["user_msg"]})
            
            # Get response from our agent
            response = chat(history)
            
            # 1. Schema check
            is_compliant = isinstance(response, dict) and "reply" in response and "recommendations" in response and "end_of_conversation" in response
            if not is_compliant:
                schema_compliance_errors += 1
                print(f"  [Turn {turn['turn_num']}] SCHEMA ERROR: {response}")
                
            # 2. Recommendations & Recall@10
            expected = [norm_url(u) for u in turn["expected_urls"]]
            predicted = [norm_url(rec["url"]) for rec in response.get("recommendations", [])]
            
            if len(expected) > 0:
                intersection = set(expected).intersection(set(predicted))
                recall = len(intersection) / len(expected)
                total_recall += recall
                total_turns_with_recs += 1
                print(f"  [Turn {turn['turn_num']}] Recs Expected: {len(expected)} | Pred: {len(predicted)} | Recall: {recall:.2f}")
                if recall < 1.0:
                    print(f"    Expected URLs: {expected}")
                    print(f"    Predicted URLs: {predicted}")
            else:
                # Expect empty recommendations
                if len(predicted) == 0:
                    recall = 1.0
                else:
                    recall = 0.0
                    print(f"  [Turn {turn['turn_num']}] BEHAVIOR ERROR: Expected 0 recommendations (clarification/refusal), but agent returned {len(predicted)} recs.")
                # We don't count turns where no recs were expected in average Recall@10, but we flag behavior
            
            # 3. EOC check
            expected_eoc = turn["expected_eoc"]
            pred_eoc = response.get("end_of_conversation", False)
            if expected_eoc == pred_eoc:
                eoc_matches += 1
            else:
                print(f"  [Turn {turn['turn_num']}] EOC Mismatch: Expected {expected_eoc} | Pred {pred_eoc}")
            total_eoc_checks += 1
            total_turns_evaluated += 1
            
            # Append trace's expected Agent reply to maintain trace state
            history.append({"role": "assistant", "content": turn["agent_msg"]})
            
    avg_recall = (total_recall / total_turns_with_recs) * 100 if total_turns_with_recs > 0 else 100.0
    eoc_accuracy = (eoc_matches / total_eoc_checks) * 100 if total_eoc_checks > 0 else 100.0
    
    print("\n" + "=" * 60)
    print("EVALUATION RESULTS SUMMARY")
    print("=" * 60)
    print(f"Average Recall@10:       {avg_recall:.2f}%")
    print(f"EOC Accuracy:            {eoc_accuracy:.2f}%")
    print(f"Schema Compliance Errors: {schema_compliance_errors}")
    print(f"Total Turns Evaluated:    {total_turns_evaluated}")
    print("=" * 60)


if __name__ == '__main__':
    run_evaluation()
