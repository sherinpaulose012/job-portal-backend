from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import SignupSerializer
from .permissions import IsAdmin, IsEmployer, IsCandidate

User = get_user_model()


# ---------------- SIGNUP ----------------
class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            {
                "success": True,
                "message": "User created successfully"
            },
            status=status.HTTP_201_CREATED
        )


# ---------------- LOGIN ----------------
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {
                    "success": False,
                    "message": "Email and password are required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": "Invalid credentials"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.check_password(password):
            return Response(
                {
                    "success": False,
                    "message": "Invalid credentials"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "success": True,
                "message": "Login successful",
                "data": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            },
            status=status.HTTP_200_OK
        )

# ---------------- PROFILE ----------------
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "email": request.user.email,
            "role": request.user.role,
        })


# ---------------- ADMIN ----------------
class AdminDashboardView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        return Response({"message": "Admin access granted"})


# ---------------- EMPLOYER ----------------
class EmployerDashboardView(APIView):
    permission_classes = [IsEmployer]

    def get(self, request):
        return Response({"message": "Employer access granted"})


# ---------------- CANDIDATE ----------------
class CandidateDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        return Response({
            "message": "Candidate access granted",
            "id": pk
        })