from rest_framework.response import Response
from .models import Challenge
from .serializers import ChallengeSerializer
from rest_framework.decorators import api_view, permission_classes
import requests 
from rest_framework.permissions import IsAuthenticated
from progress.models import UserProgress
import json
import time
from django.contrib.auth import get_user_model

User = get_user_model() 
#Response(data, status=None, template_name=None, headers=None, content_type=None)
 
JUDGE0_URL = "https://judge0-ce.p.rapidapi.com/submissions"
headers = {
    'x-rapidapi-key': "c5306512famsh0fc65a5e197c55dp1669dbjsnf044e2b6187f",
    'x-rapidapi-host': "judge0-ce.p.rapidapi.com",
    'Content-Type': "application/json"
}

@api_view(['GET'])
def challengeViewSet(request):
    challenges = Challenge.objects.all()
    queryset = ChallengeSerializer(challenges, many=True)
    return Response(queryset.data)

@api_view(["GET"])
def getChallenge(request, id):
    challenge = Challenge.objects.get(id=id)
    queryset = ChallengeSerializer(challenge, many=False)
    return Response(queryset.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def verify_solution(request, challenge_id):
    try:
        user_code = request.data.get("code")
        challenge = Challenge.objects.get(id=challenge_id)
        test_cases = challenge.test_cases
        user = request.user

        failed_cases = []

        for case in test_cases:
            # Prepare input correctly
            formatted_input = case["input"].replace(", ", "\n")

            payload = {
                "source_code": user_code,
                "language_id": 63,  # Python 3
                "stdin": formatted_input,
                "expected_output": case["expected_output"].strip(),
            }

            # Submit to Judge0
            response = requests.post(f"{JUDGE0_URL}?base64_encoded=false", json=payload, headers=headers)
            submission = response.json()

            token = submission.get("token")
            if not token:
                return Response({"error": "Judge0 did not return a valid token"}, status=400)

            # Wait and fetch result
            time.sleep(1)  # Small delay to let Judge0 process the request
            while True:
                result_response = requests.get(f"{JUDGE0_URL}/{token}?base64_encoded=false", headers=headers)
                result = result_response.json()

                if result.get("status", {}).get("id") in [3, 4]:  # 3 = Accepted, 4 = Wrong Answer
                    break
                time.sleep(1)  # Retry until execution completes

            # Check the result
            if "stdout" not in result or result["stdout"].strip() != case["expected_output"].strip():
                failed_cases.append({
                    "input": case["input"],
                    "expected_output": case["expected_output"],
                    "received_output": result.get("stdout", "").strip(),
                    "error": result.get("stderr") or result.get("compile_output", "Unknown Error")
                })

        # If all test cases passed
        if not failed_cases:
            UserProgress.objects.update_or_create(
                user=user, challenge=challenge,
                defaults={"status": "completed"}
            )
            User.objects.update_or_create(
                id=user.id, 
                defaults={
                    "points": user.points + challenge.points,  # Add challenge points to current points
                    "challenges_completed": user.challenges_completed + 1  # Increment completed challenges
                }
            )
            
            return Response({"message": "✅ Challenge Passed!", "status": "completed"})

        return Response({"message": "❌ Challenge Failed!", "failed_cases": failed_cases})

    except Challenge.DoesNotExist:
        return Response({"error": "Challenge not found"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


