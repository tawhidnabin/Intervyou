"""
Quick backend smoke test. Run with: python test_backend.py
Requires the Flask server to be running on port 5000.
"""
import requests
import os

BASE = 'http://localhost:5000/api'
TEST_EMAIL = 'testuser@example.com'
TEST_PASSWORD = 'TestPass123'
TEST_NAME = 'Test User'


def main():
    # 1. Register
    print('1. Registering user...')
    r = requests.post(f'{BASE}/auth/register', json={
        'email': TEST_EMAIL, 'password': TEST_PASSWORD, 'name': TEST_NAME
    })
    if r.status_code == 409:
        print('   User already exists, logging in instead.')
    else:
        print(f'   Register: {r.status_code} {r.json()}')

    # 2. Login
    print('2. Logging in...')
    r = requests.post(f'{BASE}/auth/login', json={
        'email': TEST_EMAIL, 'password': TEST_PASSWORD
    })
    assert r.status_code == 200, f'Login failed: {r.text}'
    token = r.json()['token']
    headers = {'Authorization': f'Bearer {token}'}
    print(f'   Token obtained.')

    # 3. Fetch questions
    print('3. Fetching questions...')
    r = requests.get(f'{BASE}/questions/', headers=headers)
    assert r.status_code == 200
    questions = r.json()
    print(f'   Got {len(questions)} questions.')
    first_q = questions[0]

    # 4. Start session
    print('4. Starting session...')
    r = requests.post(f'{BASE}/sessions/start', json={'job_role': 'Software Engineer'}, headers=headers)
    assert r.status_code == 201
    session_id = r.json()['session_id']
    print(f'   Session ID: {session_id}')

    # 5. Submit audio (dummy wav bytes)
    print('5. Submitting dummy audio...')
    # Create a minimal valid WAV file (44 bytes header + silence)
    import struct, wave, io
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(16000)
        wf.writeframes(b'\x00\x00' * 16000)  # 1 second silence
    buf.seek(0)

    r = requests.post(
        f'{BASE}/analysis/submit',
        headers=headers,
        files={'audio': ('test.wav', buf, 'audio/wav')},
        data={'session_id': str(session_id), 'question_id': str(first_q['id'])}
    )
    print(f'   Analysis response ({r.status_code}):')
    import json
    print(json.dumps(r.json(), indent=2))

    # 6. Complete session
    print('6. Completing session...')
    r = requests.post(f'{BASE}/sessions/{session_id}/complete', headers=headers)
    print(f'   Complete: {r.status_code} {r.json()}')

    print('\nAll tests passed.')


if __name__ == '__main__':
    main()
