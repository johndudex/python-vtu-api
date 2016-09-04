from vtu.processors.generic import GenericVtuResultsProcessor
import re
from bs4 import BeautifulSoup
import requests

class RegularResultProcessor(GenericVtuResultsProcessor):
    """
    Handles requests for regular results without backlogs.
    """
    def __init__(self, usn, output_format):
        self.usn = usn
        self.output_format = output_format

    def parse_html_response(self, html_response):
        result = {}

        soup = BeautifulSoup(html_response, 'html.parser')
        results_table = soup.find('td', {'width': '513'})
        bold_tags = results_table.findAll('b')

        italic_tags = results_table.findAll('i')
        subjects = [tag.text for tag in italic_tags]
        try :
            result['name'] = re.search(r'^[a-zA-Z\s]+', bold_tags[0].text).group(0).strip()
            result['result'] = bold_tags[3].text[10:].strip()
            result['usn'] = self.usn
            semester= bold_tags[2].text
            semester_list=[]
            length=len(bold_tags)
            for i in range(length):
                if bold_tags[i].text =="Semester:":
                    semester_list.append(bold_tags[i+1].text)
            #result['semester'] = bold_tags[2].text
            result["marksheet"] = []

            tags_with_marks = results_table.findAll('td', {'width': '60'})
            tags_with_marks = tags_with_marks[4:]  # Remove 'Internal', 'External', 'Total' and 'Result'

            index = 0
            lastIndex = len(tags_with_marks)
            totalmarks = 0
            sem_iter=0

            for subject in subjects:
                if index >= lastIndex:
                    break

                if tags_with_marks[index +3].text =="Result":
                    sem_iter+=1
                    semester=semester_list[sem_iter]
                    index+=4
                result["marksheet"].append({
                'subject': subject,
                'semester':semester,
                'internal': tags_with_marks[index].text,
                'external': tags_with_marks[index + 1].text,
                'total': tags_with_marks[index + 2].text,
                'result': re.search(r'P|F', tags_with_marks[index + 3].text).group()
                })

            # Update totalmarks and tagindex
                totalmarks += int(tags_with_marks[index + 2].text)
                index += 4

            result['total'] = totalmarks
            return result
        except IndexError:
            return
    @staticmethod
    def fetch_cbcs_results(usn,sem,results_type='regular'):
                    marks_list=[]
                    result= {}
                    site="http://result.vtu.ac.in/cbcs_results2016.aspx?usn="+usn+"&sem="+str(sem)
                    req=requests.post(site)
                    soup=BeautifulSoup(req.text,'lxml')
                    input=soup.findAll("input")
                    try:
                        for k in range(len(input)):
                            if input[k]['value'].upper().strip()==usn.upper().strip():
                                name_at=k
                                name=input[k-1]['value'].upper().strip()
                        k=3
                        while (k < name_at-4):
                            #pdb.set_trace()
                            subject=input[k+0]['value'].upper().strip().replace(',','')
                            code= input[k+1]['value'].upper().strip()
                            credits=input[k+2]['value'].upper().strip()
                            credits_earned=input[k+3]['value'].upper().strip()
                            grade_letter=input[k+4]['value'].upper().strip()
                            grade_points=input[k+5]['value'].upper().strip()
                            credits_points=input[k+6]['value'].upper().strip()
                            remarks=input[k+7]['value'].upper().strip()
                            marks=[subject,code,credits,credits_earned,grade_letter,grade_points,credits_points,remarks]
                            marks_list.append(marks)
                            k+=8
                    except KeyError:
                        return None
                    result['name']=name
                    result['marksheet']=marks_list
                    return result
