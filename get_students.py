import requests
import dotenv
import os
import json
from canvasapi import Canvas

dotenv.load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

COURSE_CODES = [89487, 89463, 89525, 89553, 90521, 92003] 

def fetch_students():
    canvas = Canvas('https://csulb.instructure.com', API_TOKEN)
    students_info = {}

    for course_code in COURSE_CODES:
        course = canvas.get_course(course_code)
        students = course.get_users(enrollment_type=['student'])
        
        for student in students:
            if student.name not in students_info:
                start_year = student.created_at_date.year
                if student.created_at_date.month >= 8:
                    start_year = student.created_at_date.year + 1

                students_info[student.name] = {
                    'id': student.id,
                    'courses': [],
                    'num_matching_courses': 0,
                    'created_at': str(student.created_at_date),
                    'start_year': start_year
                }
            students_info[student.name]['courses'].append(course.name)
            students_info[student.name]['num_matching_courses'] = len(students_info[student.name]['courses'])

    
    students_info = dict(sorted(students_info.items(), key=lambda item: item[1]['num_matching_courses'], reverse=True))

    with open('students.json', 'w') as json_file:
        json.dump(students_info, json_file)

    print('File saved')

def display_students():
    with open('students.json') as json_file:
        students = json.load(json_file)
        print(f'{"Name":<30}{"ID":<10}{"Courses":<10}')
        for student in students:
            print(f'{student:<30}{students[student]["id"]:<10}{students[student]["courses"]}')

def main():
    refetch_students = input('Fetch students? (y/N): ')
    if refetch_students.lower() == 'y':
        fetch_students()
    # display_students()

if __name__ == '__main__':
    main()