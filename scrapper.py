from bs4 import BeautifulSoup
import requests

LIMIT = 50

def max_page_finder(url,start=0):
  indeed_url = f"{url}&start={start * 50}"
  indeed_result = requests.get(indeed_url)

  indeed_soup = BeautifulSoup(indeed_result.text, "html.parser")
  pagination = indeed_soup.find("div", {"class": "pagination"})

  links = pagination.find_all("a")
  pages = []
  for link in links:
    if link.string:
      pages.append(int(link.string))
      max_page = pages[-1]

  next_button = pagination.find("a", {"aria-label": "다음"})
  if next_button:
    return max(max_page, max_page_finder(url,max_page + 1))
  else:
    return max_page


def extract_job(html):
  jks=[]
  a_jk = html.find_all('a',recursive=False)
  for jk in a_jk:
    jks.append(jk['data-jk'])
  
  results = []
  tables = html.find_all("table",{"class":"jobCard_mainContent"})
  for table in tables:

    #title
    div_h4 = table.find("div",{"class":"heading4"})
    title = div_h4.find("span",title=True).string
    # print(title)

    #company
    div_h6 = table.find("div",{"class":"heading6"})
    company_span = div_h6.find("span",{"class":"companyName"})
    if company_span is not None:
      company = company_span.string
    else: 
      company = div_h6.find("div",{"class":"companyLocation"}).string
    

    #location
    loca_h6 = table.find("div",{"class":"heading6"})
    location = loca_h6.find("div",{"class":"companyLocation"}).string

    results.append({"title" : title, "company" : company,"location":location})
  i = 0
  for bef_result in results:
    if len(jks) >i:
      bef_result['link'] = 'https://kr.indeed.com/%EC%B1%84%EC%9A%A9%EB%B3%B4%EA%B8%B0?jk=' +jks[i] +' '
    else:
      bef_result['link'] = ''
    i += 1
  return results

def extra_indeed_jobs(last_page,url):
  jobs = []
  for page in range(last_page):
    print(f'start page : {page}')
    result = requests.get(f"{url}&start={page*LIMIT}")
    soup = BeautifulSoup(result.text, "html.parser")
    result_div = soup.find_all("div",{"id":"mosaic-provider-jobcards"})

    for div in result_div:
      result = extract_job(div)
      jobs=jobs+result
  return jobs
    

      
def get_indeed_job(word):
  url = f"https://kr.indeed.com/jobs?q={word}&limit={LIMIT}&filter=0"
  max_page = max_page_finder(url)
  indeed_jobs = extra_indeed_jobs(max_page,url) 

  return indeed_jobs




