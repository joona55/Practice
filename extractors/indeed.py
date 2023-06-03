from requests import get
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
"""
options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
"""
##파이썬 내장 브라우저를 사용하기 위한 작업

def get_page_count(keyword):
  options = Options()
  options.add_argument("--no-sandbox")
  options.add_argument("--disable-dev-shm-usage")
  
  base_url = "https://kr.indeed.com/jobs?q="
  #기본 URL
  browser = webdriver.Chrome(options=options)
  browser.get(f"{base_url}{keyword}")
  #내가 찾을 키워드를 검색한 결과
  
  soup = BeautifulSoup(browser.page_source, "html.parser")
  pagination = soup.find("nav", class_="ecydgvn0")
  #html 코드를 가져와 그 안에 있는 페이지 번호를 포함하는 태그 찾기
  
  if pagination == None:
    return 1;
    #만약 없다면 기본값인 1을 리턴
  pages = pagination.find_all("div", recursive=False)
  #웹 화면에 보이는 페이지 버튼 수를 찾는다
  count = len(pages)
  #크롤링할 최대 페이지 수를 저장한다.
  if count >= 3:
    return 3
  else:
    return count

def extract_indeed_job(keyword):
  pages = get_page_count(keyword)
  print("Found", pages, "pages")
  for page in range(pages):
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    base_url = "https://kr.indeed.com/jobs"
    final_url = f"{base_url}?q={keyword}&start={page*10}"
    print("Requesting", final_url)
    browser = webdriver.Chrome(options=options)
    browser.get(final_url)
    
    results = []
    soup = BeautifulSoup(browser.page_source, "html.parser")
    job_list = soup.find("ul", class_="jobsearch-ResultsList")
    jobs = job_list.find_all('li', recursive=False)
    for job in jobs:
      zone = job.find("div", class_="mosaic-zone")
      if zone == None:
        anchor = job.select_one("h2 a")
        
        title = anchor['aria-label']
        link = anchor['href']
        company = job.find("span", class_="companyName")
        location = job.find("div", class_="companyLocation")
        
        job_data = {
          'link': f"https://kr.indeed.com{link}",
          'company': company.string.replace(",", " "),
          'location': location.string.replace(",", " "),
          'position': title.string.replace(",", " "),
        }
        
        results.append(job_data)
## 현재 봇으로 잡아서 에러