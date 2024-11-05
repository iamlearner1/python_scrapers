import requests
import json

# Define the GraphQL endpoint
graphql_endpoint = "http://localhost:5002/graphql"

# Authorization token
headers = {
    "Authorization": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjAyMTAwNzE2ZmRkOTA0ZTViNGQ0OTExNmZmNWRiZGZjOTg5OTk0MDEiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiU2hpdmFrdW1hciBSZWRkeSIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NJQ050aHRQOVNmc0VwTEtEaThXOXh3akNneDZiemR4azJMY1c4Wldzd0ktSGsyUzlJPXM5Ni1jIiwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL2VzY2hvb2wtZGV2LTRjNmI0IiwiYXVkIjoiZXNjaG9vbC1kZXYtNGM2YjQiLCJhdXRoX3RpbWUiOjE3MjEwMjI4MDYsInVzZXJfaWQiOiI5MWxOT3pMeFZCUUo5NTU4Zlp1WTFDR1dWcHQyIiwic3ViIjoiOTFsTk96THhWQlFKOTU1OGZadVkxQ0dXVnB0MiIsImlhdCI6MTcyNjU2OTE2OSwiZXhwIjoxNzI2NTcyNzY5LCJlbWFpbCI6Impha2thc2hpdmFrdW1hcjIyMkBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJnb29nbGUuY29tIjpbIjEwNDMxMTE0OTE4MTk0MDMyMDMxNyJdLCJlbWFpbCI6WyJqYWtrYXNoaXZha3VtYXIyMjJAZ21haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoiZ29vZ2xlLmNvbSJ9fQ.MIBpk2ByJLfSf6uB3XXA4uOf8WEwDVhSOudC1dLcUHiEP3W90ZgjFOptAo7iM19BmNAIqJ4oa9vnn-LZqVucYw7zhDVDa04jFUfBvI1XrfB8vD720EuAusbmrZBZAcAs-sCxRn-AmgLfAk_EpVS3WSUsF3RWXWqr1ZpHZbh6WTWrPBWkZsy4oJoGI-Q5R8oMNotoMJeVOxvp_HdSPI0U9gIleeQj-H0UnW7DgO7kbHtJGNiNAybV3QNGL0BH9uBUmW9QscQQ_DBFzOlw1GwyaKmP0dgTTLYkVcBbl9-gIaHDhyvZ9XAjvxs_vT8USFTzk4RAwpHpTFVyHqyW8zQUYw"
}

# Function to get student ID by admission number
def get_student_id(admission_no):
    query = """
    query {
      getAllStudents(admission_no: "%s") {
        _id
      }
    }
    """ % admission_no

    response = requests.post(graphql_endpoint, json={'query': query}, headers=headers)
    result = response.json()
    
    if 'data' in result and result['data']['getAllStudents']:
        return result['data']['getAllStudents'][0]['_id']
    return None

# Function to create a parent
def create_parent(phone_number):
    mutation = """
    mutation {
      createParent(parentData: { school_id: "66c6de41be79b0bf750eaec1", number: "%s" }) {
        _id
      }
    }
    """ % phone_number

    response = requests.post(graphql_endpoint, json={'query': mutation}, headers=headers)
    result = response.json()
    
    if 'data' in result and result['data']['createParent']:
        return result['data']['createParent']['_id']
    return None

# Function to update a student with a new parent ID
def update_student(student_id, parent_id):
    mutation = """
    mutation {
      updateStudent(studentId: "%s", newData: { parent_ids: ["%s"] }) {
        _id
      }
    }
    """ % (student_id, parent_id)

    response = requests.post(graphql_endpoint, json={'query': mutation}, headers=headers)
    result = response.json()
    
    if 'data' in result and result['data']['updateStudent']:
        return result['data']['updateStudent']['_id']
    return None

# Input data
input_data = [
  {
    "admission_no": "5065",
    "number": "9652301990"
  },
  {
    "admission_no": "5099",
    "number": "9666200974"
  },
  {
    "admission_no": "5080",
    "number": "9014465637"
  },
  {
    "admission_no": "5804",
    "number": "7286092309"
  },
  {
    "admission_no": "5063",
    "number": "9618823673"
  }
]

# Process each entry in the input data
for entry in input_data:
    admission_no = entry['admission_no']
    phone_number = entry['number']

    # Step 1: Get the student ID
    student_id = get_student_id(admission_no)

    if student_id:
        # Step 2: Create the parent and update the student record
        parent_id = create_parent(phone_number)
        if parent_id:
            updated_student_id = update_student(student_id, parent_id)
            print(f"Updated student with ID: {updated_student_id} with new parent ID: {parent_id}")
        else:
            print(f"Failed to create parent with phone number: {phone_number}")
    else:
        print(f"Student with admission number {admission_no} not found.")
