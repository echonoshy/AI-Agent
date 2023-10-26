import json
import autogen 
import os 


def _generate_agents(agent_config):

    agents = dict()
    for agent_data in agent_config['agents']:
        agent_type = agent_data['type']
        if agent_type == 'UserProxyAgent':
            agent = autogen.UserProxyAgent(
                name=agent_data['name'],
                system_message=agent_data.get('system_message', None),
                code_execution_config=agent_data.get('code_execution_config', {}),
                human_input_mode=agent_data.get('human_input_mode', None)
            )
        elif agent_type == 'AssistantAgent':
            agent = autogen.AssistantAgent(
                name=agent_data['name'],
                system_message=agent_data.get('system_message', None),
                llm_config=llm_config
            )
        else:
            raise ValueError(f'Unsupported agent type: {agent_type}')

        agents[agent_data["name"]] = agent 

        return agents



def _load_llm_config(file="OAI_CONFIG_LIST"):
    return autogen.config_list_from_json("OAI_CONFIG_LIST")

def _load_agent_config(file):
    with open(file, "r") as f:
        data = json.load(f)
    return data 



def run(msg: str):
    
    llm_config = _load_llm_config("OAI_CONFIG_LIST")
    agent_config = _load_agent_config("/Users/hupan/Codes/KDF/gitcodes/AI-Agent/configs/no1.json")
    
    agents = _generate_agents(agent_config)

    initiate_config = data.get("start_conversation")
    initiator = agents[initiate_config.get("initiator")]
    recevior = agents[initiate_config.get("recevior")]
    initiator.initiate_chat(
        recevior,
        message=msg
    )


if __name__ == "__main__":
    msg = "今天是什么日子"
    run(msg)