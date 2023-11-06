import autogen

config_list_gpt4 = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    # filter_dict={
    #     "model": ["gpt-4"],
    # },
)


gpt4_config = {
    "seed": 22,  
    "temperature": 0,
    "config_list": config_list_gpt4,
    "timeout": 120,
}


Admin = autogen.UserProxyAgent(
    name="Admin",
    system_message="""
        A human admin. Interact with the planner to discuss the plan. 
        Plan execution needs to be approved by this admin.
    """,
    code_execution_config={
        "work_dir": "WareHouse/gomoku",
        "use_docker": False,
        "llm_config": gpt4_config
    },
)

Product_manager = autogen.AssistantAgent(
    name="Product_manager",
    llm_config=gpt4_config,
    system_message='''Product manager. you are responsible for all product issues. containing product plans, 
    breaking down product requirements and designing product features.
    You also need to revise the plan based on feedback from admin and critic, until admin approval.
    The plan may involve a programmer who can write code. explain the plan first and which step is performed by programmer.
''',
)

Critic = autogen.AssistantAgent(
    name="Critic",
    system_message="Critic. Double check plan, claims, code from other agents and provide feedback.",
    llm_config=gpt4_config,
)

Programmer = autogen.AssistantAgent(
    name="Programmer",
    llm_config=gpt4_config,
    system_message='''Programmer. You follow an approved plan. 
    you can write/create computer software or applications by providing a specific programming language to the computer.
    To complete the task, you must write a response that appropriately solves the requested instruction based on your expertise and meet the requirements.
    You write python/shell code to solve tasks. Wrap the code in a code block that specifies the script type. The user can't modify your code. 
    So do not suggest incomplete code which requires others to modify. Don't use a code block if it's not intended to be executed by the executor.
    Don't include multiple code blocks in one response. Do not ask others to copy and paste the result. Check the execution result returned by the executor.
    If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. 
    If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, 
    collect additional info you need, and think of a different approach to try.
''',
)

Code_reviewer = autogen.AssistantAgent(
    name="Code_reviewer",
    llm_config=gpt4_config,
    system_message='''Code Reviewer. You can help programmers to assess source codes for software troubleshooting, 
    fix bugs to increase code quality and robustness, and offer proposals to improve the source codes. 
    To complete the task, you must write a response that appropriately solves the requested instruction based on your expertise and meet requirements.

''',
)


Document_writer = autogen.AssistantAgent(
    name="Document_writer",
    llm_config=gpt4_config,
    system_message='''Document writer. your are working when the software or applications development done.
    you need to write the manual according to the functions and usage of the software. and save the manual to local file.
''',
)




groupchat = autogen.GroupChat(agents=[Admin, Programmer, Code_reviewer,
                              Product_manager, Document_writer, Critic], messages=[], max_round=12)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=gpt4_config)


Admin.initiate_chat(
    manager,
    message="""
请帮我实现一个五子棋游戏
""",
)
