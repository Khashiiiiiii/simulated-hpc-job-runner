*** Settings ***
Library    RequestsLibrary
Library    Collections      
Library    JobLibrary.py   

*** Variables ***
${BASE_URL}    http://localhost:8000

*** Test Cases ***
Submit Valid Job And Verify Execution
    [Documentation]    Submits a job, waits for the worker, and verifies the result.
    
    ${complexity}=    Set Variable    5
    ${payload}=       Create Dictionary    task_name=TestMatrix    complexity=${complexity}
    
    Create Session    hpc_api    ${BASE_URL}
    ${resp}=          POST On Session    hpc_api    /submit-job    json=${payload}
    Status Should Be  200    ${resp}
    
    ${job_id}=        Get From Dictionary    ${resp.json()}    job_id
    Log               Job submitted with ID: ${job_id}

    ${result}=        Wait For Job Completion    ${BASE_URL}    ${job_id}

    Should Be Equal   ${result['status']}    completed
    
    Verify Matrix Size    ${complexity}    ${result['matrix_size']}

Submit Heavy Job And Expect Rejection
    [Documentation]    Ensures the system correctly rejects complex jobs.
    
    ${payload}=       Create Dictionary    task_name=TooHard    complexity=25
    
    Create Session    hpc_api    ${BASE_URL}
    ${resp}=          POST On Session    hpc_api    /submit-job    json=${payload}
    ${job_id}=        Get From Dictionary    ${resp.json()}    job_id
    
    Run Keyword And Expect Error
    ...    *Job failed*
    ...    Wait For Job Completion
    ...    ${BASE_URL}
    ...    ${job_id}