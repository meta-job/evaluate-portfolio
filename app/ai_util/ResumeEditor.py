import os
from openai import OpenAI
from dotenv import load_dotenv
import time


load_dotenv()

class ResumeEditor:
    def __init__(self, request) -> None:
        self.request = request
        self.user_id = ""
        self.client = OpenAI(api_key = os.getenv('OPENAI_API_KEY'))
        self.assistant_id = os.getenv('ASSISTANTS_ID')
        self.thread = ""
        self.content = ""
        self.instructions = f'''
            너는 한국어로 포트폴리오를 보고 프로젝트 설명을 보충해주는 포르폴리오 작성 도우미야"
            다음 7가지 기준으로 각 프로젝트 목록을 분류해서 그 기준대로 설명이 있는지 확인해줘.
            기준대로 있으면 좀 더 보충해서 설명할 걸 넣어주고, 없으면 주어진 이력서를 토대로 넣어줘
            사람들이 작성하는 포트폴리오를
            1. 어떠한 프로젝트들을 각각 진행 했는지?
            그리고 각 프로젝트마다 밑에 질문들을 체크해줘
            1. 프로젝트를 왜 했는지?
            2. 프로젝트에 어떠한 기술을 진행했는지?
            3. 기술 선정을 할 때 타당한 이유가 있는지?
            4. 결과가 어떻게 되었는지?
            5. 프로젝트를 진행하면서 기술적인 한계 또는 문제점은 없었는지?'''
        
        self.result={}


    def __enter__(self):
        self.create_thread()
        self.create_message()
        self.run_thread()
        self.get_message()
        # self.close_thread()
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
        self.result["thread"] = self.thread

    def create_message(self):
        self.analysis_resume()
        message = self.client.beta.threads.messages.create(
            thread_id = self.thread.id,
            role="user",
            content=self.content
        )
        self.result["message"] = message


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
        self.result["run"] = run

    def get_message(self):
        self.result["final_result"] = self.client.beta.threads.messages.list(
            thread_id=self.thread.id
        )

    def close_thread(self):
        self.result["thread_close"] = self.client.beta.threads.delete(
            thread_id = self.thread.id
        )
        self.thread = ""

        
    def analysis_resume(self):
        self.project_skills = self.request["project_skill"]
        self.project_description = self.request["project_description"]
        self.content= f'''
        사용 기술은 {self.project_skills} 이고,
        설명은 {self.project_description}이야
        '''

    def set_analysis_result():
        pass
