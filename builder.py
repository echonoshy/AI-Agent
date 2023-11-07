import json
import autogen


def _generate_agents(autogen_config, config_list) -> dict:
    """
    生成代理。

    :param autogen_config: 用于生成代理的配置。
    :param config_list: 配置列表。
    :return: 字典，包含代理名和代理对象。
    """
    agents = dict()
    for agent_config in autogen_config['agents']:
        agent_type = agent_config.pop("type")
        agent_config.get("llm_config")["config_list"] = config_list

        if agent_type == 'UserProxyAgent':
            agent = autogen.UserProxyAgent(**agent_config)
        elif agent_type == 'AssistantAgent':
            agent = autogen.AssistantAgent(**agent_config)
        else:
            raise ValueError(f'Unsupported agent type: {agent_type}')

        agents[agent_config["name"]] = agent

    return agents


def _generate_groups(autogen_config, agents) -> dict:
    """
    从配置中构建代理组

    :param autogen_config: 用于生成组的配置。
    :param agents: 代理字典。
    :return: 字典，包含组名和组对象。
    """
    groups = dict()
    for group_config in autogen_config.get("groups", []):
        group_name = group_config.pop("name")
        groups[group_name] = autogen.GroupChat(
            agents=[agent_value for (agent_key, agent_value) in agents.items(
            ) if agent_key in group_config.get("grouped_agents", [])],
            messages=group_config.get("message", []),
            max_round=group_config.get("max_round", 10)
        )

    return groups


def _manage_groups(autogen_config, config_list, groups):
    """
    生成代理组manager，用于管理代理组对话

    :param autogen_config: 用于生成管理的配置。
    :param config_list: 配置列表。
    :param groups: 组字典。
    :return: 字典，包含管理名和管理对象。
    """
    managers = dict()
    for manager_config in autogen_config.get("managers", []):

        manager_config.get("llm_config")["config_list"] = config_list
        managers[manager_config["name"]] = autogen.GroupChatManager(
            groupchat=groups[manager_config.get("groupchat")],
            llm_config=manager_config.get("llm_config"),
        )

    return managers


def _load_autogen_config(file):
    """
    加载自动生成配置。

    :param file: 配置文件路径。
    :return: 配置字典。
    """
    try:
        with open(file, "r") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"The configuration {file} does not exist!")


def run(msg, config_file):
    """
    运行代理。

    :param msg: 初始化消息。
    :param config_file: 配置文件路径。
    """
    autogen_config = _load_autogen_config(config_file)
    models = autogen_config.get("models")
    config_list = autogen.config_list_from_json(
        "OAI_CONFIG_LIST",
        filter_dict={"model": models},
    )

    agents = _generate_agents(autogen_config, config_list)
    groups = _generate_groups(autogen_config, agents)
    managers = _manage_groups(autogen_config, config_list, groups)

    init_config = autogen_config.get("start_conversation")

    initiator = agents.get(init_config.get("initiator")) or managers.get(
        init_config.get("initiator"))
    recipient = agents.get(init_config.get("recipient")) or managers.get(
        init_config.get("recipient"))

    autogen.ChatCompletion.start_logging()
    initiator.initiate_chat(recipient, message=msg)
    
    # 实例化对话日志
    json.dump(autogen.ChatCompletion.logged_history, 
              open("conversations_1.json", "w", encoding='utf-8'), 
              ensure_ascii=False)


if __name__ == "__main__":
    msg = "请实现一款html贪吃蛇游戏"
    config_file = "snake_game_1.json"
    run(msg, config_file)

