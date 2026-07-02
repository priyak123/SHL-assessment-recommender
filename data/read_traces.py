import os
import re

dir_path = r'C:\Users\HELLO\.gemini\antigravity\scratch\shl_recommender\sample_conversations\GenAI_SampleConversations'

for f_name in sorted(os.listdir(dir_path)):
    if not f_name.endswith('.md'):
        continue
    path = os.path.join(dir_path, f_name)
    content = open(path, 'r', encoding='utf-8').read()
    
    print('='*50)
    print(f"Trace: {f_name}")
    print('='*50)
    
    # Let's find turns manually by splitting by '### Turn'
    turns = content.split('### Turn')[1:]
    for t in turns:
        lines = t.strip().split('\n')
        turn_num = lines[0].strip()
        
        # Extract User message
        user_msg = ""
        agent_msg = ""
        recs_status = "NO"
        
        user_idx = -1
        agent_idx = -1
        for idx, line in enumerate(lines):
            if '**User**' in line:
                user_idx = idx
            elif '**Agent**' in line:
                agent_idx = idx
        
        if user_idx != -1:
            # find next lines starting with >
            u_lines = []
            for l in lines[user_idx+1:]:
                if l.strip().startswith('>'):
                    u_lines.append(l.strip().lstrip('>').strip())
                elif l.strip() == "":
                    continue
                else:
                    break
            user_msg = " ".join(u_lines)
            
        if agent_idx != -1:
            a_lines = []
            for l in lines[agent_idx+1:]:
                if l.strip().startswith('_') or l.strip().startswith('|') or 'recommendations:' in l or 'end_of_conversation:' in l:
                    break
                a_lines.append(l.strip())
            agent_msg = " ".join([x for x in a_lines if x])
            
        # Check recommendations
        if '|' in t:
            recs_status = "YES"
            
        # Check end of conversation
        eoc = "false"
        if "end_of_conversation`: **true**" in t.lower() or "end_of_conversation: true" in t.lower():
            eoc = "true"
            
        print(f"Turn {turn_num} | User: {user_msg[:60]}...")
        print(f"       | Agent: {agent_msg[:60]}...")
        print(f"       | Recs: {recs_status} | EOC: {eoc}")
