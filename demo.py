# 实现一个软件自动开发的agent系统

import autogen 

config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        # "model": ["gpt-35-turbo-16k"],
        "model": ["gpt-4", "gpt-4-0314", "gpt4", "gpt-4-32k", "gpt-4-32k-0314", "gpt-4-32k-v0314"],
    },
)

llm_config = {
    "timeout": 180,
    "seed": 22,
    "config_list": config_list,
    "temperature": 0
}

assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config=llm_config
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="ALWAYS",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "coding/gomoku",
        "use_docker": False,  
    },
)

user_proxy.initiate_chat(
    assistant,
    message="""
    请帮我开发一款五子棋游戏，请按照如下的步骤来完成， 每一步完成并确认后再进入下一步：
    1. 对需求进行拆分，并明确每一步实现的功能。
    2. 选择编程语言并向用户确认。
    3. 根据需求编写代码。
    4. 确认代码功能是否符合用户预期。
    5. 编写文档说明，并使用shell脚本将文档保存到本地。
""",
)