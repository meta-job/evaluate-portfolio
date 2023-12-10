import os
from openai import OpenAI
from dotenv import load_dotenv
import fitz
import time
import json
import re
import ast

load_dotenv()

class PortfolioEditor:
    def __init__(self, request) -> None:
        self.request = request
        self.client = OpenAI(api_key = os.getenv('OPENAI_API_KEY'))
        self.assistant_id = os.getenv('ASSISTANTS_ID')
        self.thread = ""
        self.content = ""
        self.instructions = '''
            
            당신은 한국어로 사용자의 Portfolio를 보고 프로젝트 설명을 보충해주는 Portfolio 작성 보조자입니다." 
            각각의 프로젝트 목록을 분류하고, 프로젝트마다 다음 5가지 기준으로 설명이 되어 있는지 확인해
            프로젝트가 5가지 기준대로 있더라도 당신이 조금 더 추가적으로 설명을 넣어주고, 추가로 설명해준 내용을 꼭 표시해줘. 
            다만, 5가지 기준에 없으면 Portfolio를 추가로 설명할 수 있게 작성해주고 추가된 부분을 표시해.
            다음은 프로젝트 설명이야 0번은 프로젝트 분류.
            0. 어떠한 프로젝트들을 각각 진행 했는지?
            그리고 각 프로젝트마다 밑에 질문들을 체크해줘
            1. 프로젝트를 왜 했는지?
            2. 프로젝트에 어떠한 기술을 진행했는지?
            3. 프로젝트의 기술 선정을 할 때, 선정한 기술의 타당한 이유가 있는지?
            4. 프로젝트 결과가 어떻게 되었는지?
            5. 프로젝트를 진행하면서 기술적인 한계 또는 문제점은 없었는지?
            
            위의 설명은
            result={
                project_1:{
                0:"",1:"", 2:"", 3:"", 4:"", 5:""
                }
            }
            의 형식으로 보여주되,
            만약 프로젝트가 더 있으면
            project_number:{
                0:"",1:"", 2:"", 3:"", 4:"", 5:""
                }를 추가해서 결과를 보여줘
            
            '''
        self.answer  = ""
        self.result={}


    def __enter__(self):
        self.create_thread()
        self.run_thread()
        self.get_message()
        self.close_thread()
        self.set_analysis_result()
        return self.result

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def create_assistant(self):
        self.assistant = self.client.beta.assistants.create(
            name="portfolio tutor",
            instructions = self.instructions,
            model="gpt-4-1106-preview",
            tools=[{"type": "retrieval"}]
        )

    def create_thread(self):
        self.my_question()
        # if self.request["portfolio_file"]:
        #     file_to_send = self.client.files.create(
        #         file=open(self.request["portfolio_file"], "rb"),
        #         purpose="assistants"
        #     )


        #     thread = self.client.beta.threads.create(
        #         messages=[
        #             {"role": "user",
        #             "content": self.content,
        #             "file_ids" : [file_to_send.id]
        #             }
        #         ]
        #     )
        #     self.result["portfolio_file_id"] = file_to_send.id

        # else:
        thread = self.client.beta.threads.create(
            messages=[
                {"role": "user",
                "content": self.content
                }
            ]
        )
        self.result["portfolio_file_id"] = ""
        self.thread = thread

    def run_thread(self):
        run = self.client.beta.threads.runs.create(
            thread_id = self.thread.id,
            assistant_id = self.assistant_id
        )
        while run.status != "completed":
            if run.status in ["cancelling", "cancelled", "failed"]:
                return
            time.sleep(1)
            run = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread.id,
                run_id=run.id
            )

    def get_message(self):
        self.answer = self.client.beta.threads.messages.list(
            thread_id=self.thread.id
        )
        #  "SyncCursorPage[ThreadMessage](data=[ThreadMessage(id='', assistant_id='asst_Jkaw9M3DoB8CGn8A6XYNaXIG', content=[MessageContentText(text=Text(annotations=[], value='파일이 업로드되지 않았어요. 제가 당신의 포트폴리오를 도와드리기 위해서는 먼저 포트폴리오 파일이 필요합니다. 파일을 업로드해주시면, 그에 맞춰 프로젝트 리스트를 분석하고 각각의 세부 사항을 확인하여 더욱 세심하고 정교한 설명을 보완해드릴 수 있을 거에요. 파일을 업로드 후 다시 요청해주세요!'), type='text')], created_at=1701827537, file_ids=[], metadata={}, object='thread.message', role='assistant', run_id='', thread_id=''), ThreadMessage(id='', assistant_id=None, content=[MessageContentText(text=Text(annotations=[], value='\\n        주어진 설명은 다음과 같아\\n        사용 기술은 python, flask, openai, whisper, spring 이고,\\n        프로젝트 설명은 다음과 같아 베트남 개발자를 위한 한국어 교육 솔루션을 제공하고자 개발했습니다.\\n\\nspring으로 안정적인 서버를 구현하고자했고, flask, python은 ai에최적화된 라이브러리를 사용한 모델 이용을 위해 사용했습니\\n        '), type='text')], created_at=1701827535, file_ids=[], metadata={}, object='thread.message', role='user', run_id=None, thread_id='')], object='list', first_id='', last_id='', has_more=False)" 

    def close_thread(self):
        self.client.beta.threads.delete(
            thread_id = self.thread.id
        )
        self.thread = ""

        
    def my_question(self):
        self.project_description = self.request["project_description"] if self.request["project_description"] else ""
        list_of_project = self.project_description

        if type(self.project_description) == "str":
            list_of_project = ast.literal_eval()
            for i in range(len(list_of_project)):
                self.content += f"주어진 프로젝트 {i+1} 번째: 사용 스킬은 {list_of_project[i][0]}, 설명은 '{list_of_project[i][1]}' 입니다."

        elif len(list_of_project) > 0:
            for i in range(len(list_of_project)):
                self.content += f"주어진 프로젝트 {i+1} 번째: 사용 스킬은 {list_of_project[i][0]}, 설명은 '{list_of_project[i][1]}' 입니다."



    def set_analysis_result(self):
        # pattern = re.compile(r'"project_[0-9]+":\s*{([^}]+)}', re.DOTALL)
        # matches = pattern.findall(str(self.answer))
        # self.result["answer"] = {"match": matches}
        result = self.answer.data[0].content[0].text.value

        pattern_json = re.compile(r'```json(.*?)```', re.DOTALL)
        pattern_result = re.compile(r'result\s*=\s*({.*?})', re.DOTALL)
        pattern_project = re.compile(r'"project_[0-9]+":\s*{([^}]+)}', re.DOTALL)

        json_match = re.search(pattern_json, result)
        result_match = re.search(pattern_result, result)
        project_match = re.search(pattern_project, result)

        if result.startswith("result"):
            self.result["answer"] = result
        elif json_match:
            self.result["answer"] = json_match.group() if json_match else None
        elif result_match:
            self.result["answer"] = result_match.group() if result_match else None
        elif project_match:
            self.result["answer"] = project_match.group() if project_match else None
        else:
            self.result["answer"] = result