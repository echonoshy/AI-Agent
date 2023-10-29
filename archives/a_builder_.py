import json
import autogen 




def _generate_agents(autogen_config, config_list):

    agents = dict()
    for agent_config in autogen_config['agents']:
        agent_type = agent_config.pop("type")
        agent_config.get("llm_config")["config_list"] = config_list

        if agent_type == 'UserProxyAgent':

            agent = autogen.UserProxyAgent(
                **agent_config
                # name=agent_config['name'],
                # is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
                # max_consecutive_auto_reply=agent_config.get("max_consecutive_auto_reply", None),
                # human_input_mode=agent_config.get("human_input_mode", "ALWAYS"),
                # function_map=agent_config.get('function_map', None),
                # code_execution_config=agent_config.get('code_execution_config', None),
                # default_auto_reply=agent_config.get("default_auto_reply", None),
                # llm_config= agent_config.get("llm_config", False),
                # system_message=agent_config.get('system_message', "")
            )
        elif agent_type == 'AssistantAgent':

            agent = autogen.AssistantAgent(
                **agent_config
            )
        else:
            raise ValueError(f'Unsupported agent type: {agent_type}')

        agents[agent_config["name"]] = agent 

    return agents


def _generate_groups(autogen_config, agents):
    groups = dict()
    for group_config in autogen_config.get("groups"):
        group_name = group_config.pop("name")
        groups[group_name] = autogen.GroupChat(

            agents=[agent_value for (agent_key, agent_value) in agents.items() if agent_key in group_config["grouped_agents"]],
            messages=group_config.get("message", []),
            max_round=group_config.get("max_round", 10)
        )
        
    return groups


def _manage_groups(autogen_config, config_list, groups):
    managers = dict()
    for manager_config in autogen_config.get("managers"):

        manager_config.get("llm_config")["config_list"] = config_list
        managers[manager_config["name"]] = autogen.GroupChatManager(
            groupchat=groups[manager_config.get("groupchat")],
            llm_config=manager_config.get("llm_config"),
        )

    return managers



def _load_autogen_config(file="OAI_CONFIG_LIST"):
    try:
        with open(file, "r") as f:
            data = json.load(f)
        return data 
    except FileNotFoundError:
        raise FileNotFoundError(f"The configuration {file} does not exist!")




def run(msg, config_file):

    autogen_config = _load_autogen_config(config_file)
    models = autogen_config.get("models")
    config_list = autogen.config_list_from_json(
        "OAI_CONFIG_LIST", 
        filter_dict={
            "model": models,
        }
    )

    agents = _generate_agents(autogen_config, config_list)

    if autogen_config.get("groups"):
        groups = _generate_groups(autogen_config, agents)
        managers = _manage_groups(autogen_config, config_list, groups)

    init_config = autogen_config.get("start_conversation")

    # 判断这些agent是否是组或者manager
    if init_config.get("initiator") in agents:
        initiator = agents[init_config.get("initiator")]
    else:
        initiator = managers[init_config.get("initiator")]
    
    if init_config.get("recipient") in agents:
        recipient = agents[init_config.get("recipient")]
    else: 
        recipient = managers[init_config.get("recipient")]

    initiator.initiate_chat(
        recipient,
        message=msg  
    )

if __name__ == "__main__":
    msg = "请帮我实现一个python版本的贪吃蛇游戏"
    config_file = "snake_game_2.json" 
    run(msg, config_file)
