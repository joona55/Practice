from requests import get
from bs4 import BeautifulSoup

def extract_wwr_jobs(keyword):
  base_url = "https://weworkremotely.com/remote-jobs/search?term="
  response = get(f"{base_url}{keyword}")
  #url을 키워드와 조합하여 원하는 페이지 입력
  
  if response.status_code != 200: #만약 코드가 200이 아니라면
    print("Can't request website")
  else:
    results = [] 
    #리스트 생성
    soup = BeautifulSoup(response.text, "html.parser") 
    #html 코드 가져오기
    jobs = soup.find_all('section', class_="jobs") 
    #html 코드 중 section 태그 내 jobs 클래스에 있는 것 가져오기
    for job_section in jobs:
      job_posts = job_section.find_all('li')
      job_posts.pop(-1)
      #불필요한 view-all 태그를 제외한 모든 li 목록 가져오기
      for post in job_posts:
        anchors = post.find_all('a')
        #li 태그내 a 태그를 가진 모든 항목 가져오기
        anchor = anchors[1]
        #필요한 a 태그를 anchor에 할당
        link = anchor['href']
        company, kind, region = anchor.find_all('span', class_="company")
        #company로 겹치는 클래스를 분리해줌
        title = anchor.find('span', class_="title")
        #title 클래스를 변수에 할당
        job_data = {
          'link': f"https://weworkremotely.com{link}",
          'company': company.string.replace(",", " "),
          'location': region.string.replace(",", " "),
          'position': title.string.replace(",", " ")
        }
        results.append(job_data)
        #딕셔너리를 만들어서 리스트에 넣어줌
    return results