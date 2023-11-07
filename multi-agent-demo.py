import autogen
import json 


config_list_gpt4 = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-4"],
    },
)


gpt4_config = {
    "seed": 22,  
    "temperature": 0,
    "config_list": config_list_gpt4,
    "timeout": 120,
}


Admin = autogen.UserProxyAgent(
    name="Admin",
    human_input_mode="ALWAYS",
    max_consecutive_auto_reply=20,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "WareHouse/gomoku",
        "use_docker": False
    },
)

Product_manager = autogen.AssistantAgent(
    name="Product_manager",
    llm_config=gpt4_config,
    system_message='''Product manager. you are responsible for all product issues. containing product plans, 
    breaking down product requirements and designing product features.
    You also need to revise the plan based on feedback from admin and critic, until admin approval.

''',
)

Critic = autogen.AssistantAgent(
    name="Critic",
    system_message="""Critic. 
    Double check plan, claims, code from other agents and provide feedback.
    """,
    llm_config=gpt4_config,
)

Programmer = autogen.AssistantAgent(
    name="Programmer",
    llm_config=gpt4_config,
    system_message='''Programmer.
    You write python/shell code to solve tasks. Wrap the code in a code block that specifies the script type. The user can't modify your code. 
    So do not suggest incomplete code which requires others to modify. Don't use a code block if it's not intended to be executed by the executor.
    Don't include multiple code blocks in one response. Do not ask others to copy and paste the result. Check the execution result returned by the executor.
    If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. 
    If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, 
    collect additional info you need, and think of a different approach to try.
    if your code have many files, please make sure all the file in the same folder. after admin think code is ok, please save all code in the target folder.
''',
)

Code_reviewer = autogen.AssistantAgent(
    name="Code_reviewer",
    llm_config=gpt4_config,
    system_message='''Code Reviewer. 
    only when the programmer provides executable code block,
    you start to work: help to find the bugs and improve the code quality.

''',
)


Document_writer = autogen.AssistantAgent(
    name="Document_writer",
    llm_config=gpt4_config,
    system_message='''Document writer. 
    only when the admin ensure all software functions are reached and all code without bugs, you start to work:
    you need to write the README.md in the follow template:
    1. title of application/software
    2. descriptions and features
    3. how to install and start
    you also need to finish the related documents such as gitignore if needed. when all documents are done, let admin to check.
''',
)




groupchat = autogen.GroupChat(agents=[Admin, Programmer, Code_reviewer,
                              Product_manager, Document_writer, Critic], messages=[], max_round=50)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=gpt4_config)

autogen.ChatCompletion.start_logging()

try: 
    Admin.initiate_chat(
        manager,
        message="""
    请帮我实现一个五子棋游戏
    """,
    )
except Exception as e:
    print(e)
finally:
    with open("log.log", "w", encoding="utf-8") as f:
        f.write(json.dumps(autogen.ChatCompletion.logged_history, ensure_ascii=False))
