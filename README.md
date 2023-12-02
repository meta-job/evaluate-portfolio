# 도커를 활용한 로컬 실행
프로젝트 루트에서


docker build -t resume_feedback .
docker run -d -p 8000:8000 -v `pwd`:/usr/src/app --name resume_feedback resume_feedback


실행하면 docker에서 resume_feeback 컨테이너 생성됩니다

localhost:8000에서 
{"Hello" : "World"} 페이지가 나오면 성공적으로 호스트와 컨테이너가 연결된겁니다
