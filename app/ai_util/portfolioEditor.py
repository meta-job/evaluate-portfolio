import os
from openai import OpenAI
from dotenv import load_dotenv
import time
import json
import re

load_dotenv()

class PortfolioEditor:
    def __init__(self, request) -> None:
        self.request = request
        self.client = OpenAI(api_key = os.getenv('OPENAI_API_KEY'))
        self.assistant_id = os.getenv('ASSISTANTS_ID')
        self.thread = ""
        self.content = ""
        self.instructions = f'''
            너는 한국어로 포트폴리오용 프로젝트 설명을 보충해주는 포르폴리오 작성 도우미야.
            주어진 설명에 대해서 다음 7가지 기준대로 설명이 있는지 확인해줘.
            기준대로 있으면 좀 더 보충해서 설명할 걸 넣어주고, 없으면 주어진 이력서를 토대로 넣어줘
            사람들이 작성한 프로젝트 설명에 다음 질문의 양식과 똑같이 체크해줘
            # 1. 프로젝트를 왜 했는지?
            # 2. 프로젝트에 어떠한 기술을 진행했는지?
            # 3. 기술 선정을 할 때 타당한 이유가 있는지?
            # 4. 결과가 어떻게 되었는지?
            # 5. 프로젝트를 진행하면서 기술적인 한계 또는 문제점은 없었는지?'''
        self.answer  = ""
        self.result={}


    def __enter__(self):
        self.create_thread()
        self.analysis_resume()
        self.create_message()
        self.run_thread()
        self.get_message()
        self.close_thread()
        self.set_analysis_result()
        return self.result

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    # def create_assistant(self):
    #     self.assistant = self.client.beta.assistants.create(
    #         name="portfolio tutor",
    #         instructions = self.instructions,
    #         model="gpt-4-1106-preview",
    #         tools=[{"type": "retrieval"}]
    #     )


    def create_thread(self):
        thread = self.client.beta.threads.create()
        self.thread = thread

    def create_message(self):

        file = self.client.files.create(
            file=open(self.request["portfolio_file"], "rb"),
            purpose='assistants'
            )

        message = self.client.beta.threads.messages.create(
            thread_id = self.thread.id,
            role="user",
            content=self.content,
            file_ids = [file.id]
        )


    def run_thread(self):
        run = self.client.beta.threads.runs.create(
            thread_id = self.thread.id,
            assistant_id = self.assistant_id
        )
        while run.status != "completed":
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

        
    def analysis_resume(self):
        self.project_skills = self.request["project_skill"]
        self.project_description = self.request["project_description"]

        self.content= f'''
        주어진 설명은 다음과 같아
        사용 기술은 {self.project_skills} 이고,
        프로젝트 설명은 다음과 같아 {self.project_description}
        '''

    def set_analysis_result(self):
        answer = json.dumps(str(self.answer))
        answer = json.loads(answer)
        pattern = re.compile(r"value='(.*?)'")

        match = pattern.search(answer)

        if match:
            result = match.group(0)
            result = json.dumps(result)
            result = json.loads(result)
            numbering_pattern = re.compile(r"\\n[0-9].(.*?)\\")

            numbering = numbering_pattern.search(result)

            if numbering:
                self.result["answer"] = {
                    "first": numbering.group(0),
                    "second" : numbering.group(1),
                    "third": numbering.group(2),
                    "forth" : numbering.group(3),
                    "fifth" : numbering.group(4),
                }
            else:
                self.result["answer"] = {"error": "숫자로 나누어지지 않음", "content": result}

        else:
            self.result["answer"] = {"error": "gpt의 답에서 content 가 걸러지지 않음"}