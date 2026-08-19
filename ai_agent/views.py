import os

from django.http import JsonResponse
from openai import OpenAI

from portfolio.models import (
    Profile,
    Skill,
    Project,
    Experience,
    Education,
)


def chat(request):

    if request.method != "POST":
        return JsonResponse(
            {
                "error": "Only POST requests are allowed."
            },
            status=405
        )

    question = request.POST.get("question", "").strip()

    if not question:
        return JsonResponse(
            {
                "error": "Please enter a question."
            },
            status=400
        )

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return JsonResponse(
            {
                "error": "OpenAI API key is not configured."
            },
            status=500
        )

    client = OpenAI(api_key=api_key)

    # ==========================================
    # GET PORTFOLIO DATA FROM DATABASE
    # ==========================================

    profile = Profile.objects.first()

    skills = Skill.objects.all()

    projects = Project.objects.all()

    experiences = Experience.objects.all()

    education = Education.objects.all()


    # ==========================================
    # BUILD PORTFOLIO CONTEXT
    # ==========================================

    portfolio_context = f"""
You are the AI Portfolio Assistant for Deepal.

Your job is to help visitors learn about
Deepal and her professional portfolio.

Name:
{profile.name if profile else "Deepal"}

Professional Role:
{profile.role if profile else "Python Full Stack Developer"}

About:
{profile.about if profile else ""}

Email:
{profile.email if profile else ""}

Location:
{profile.location if profile else ""}


TECHNICAL SKILLS:
"""


    for skill in skills:

        portfolio_context += f"""
- {skill.name}
  Category: {skill.category}
  Proficiency: {skill.proficiency}%
"""


    portfolio_context += """

PROJECTS:
"""


    for project in projects:

        portfolio_context += f"""
- {project.title}

Description:
{project.description}

Technologies:
{project.technologies}
"""


    portfolio_context += """

PROFESSIONAL EXPERIENCE:
"""


    for experience in experiences:

        portfolio_context += f"""
- {experience.job_title}

Company:
{experience.company}

Start Date:
{experience.start_date}

End Date:
{experience.end_date}

Description:
{experience.description}
"""


    portfolio_context += """

EDUCATION:
"""


    for item in education:

        portfolio_context += f"""
- {item.degree}

Institution:
{item.institution}

Start Year:
{item.start_year}

End Year:
{item.end_year}

Description:
{item.description}
"""


    portfolio_context += """

INSTRUCTIONS:

1. Answer questions about Deepal's portfolio
   clearly and professionally.

2. Use only the portfolio information provided
   above.

3. Do not invent personal information.

4. If the visitor asks something unrelated
   to Deepal's portfolio, politely explain that
   you specialize in answering questions about
   Deepal's professional profile.

5. Keep answers concise and easy to understand.

6. If asked "Why should I hire Deepal?",
   summarize her skills, projects, experience,
   and strengths professionally.

7. If asked about a project, mention its
   technologies and purpose when available.

8. Keep responses natural because they may be
   converted into speech.
"""


    # ==========================================
    # SEND QUESTION TO OPENAI
    # ==========================================

    try:

        response = client.responses.create(
            model="gpt-5.6-luna",
            instructions=portfolio_context,
            input=question
        )

        answer = response.output_text

        return JsonResponse(
            {
                "answer": answer
            }
        )

    except Exception as e:

        return JsonResponse(
            {
                "error": str(e)
            },
            status=500
        )