import os

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    flash,
    current_app,
    send_from_directory
)

from flask_login import (
    login_required,
    current_user
)

from werkzeug.utils import secure_filename

from database.models import db
from database.models.resume import Resume
from sqlalchemy import and_

from services.file_service import (
    allowed_file
)

from nlp.resume_parser import (
    ResumeParser
)

from services.ats_service import (
    ATSAnalyzer
)

from services.jd_matching_service import (
    JDMatcher
)

from services.career_service import (
    CareerPredictor
)

resume_bp = Blueprint(
    "resume",
    __name__
)


def _get_user_resume(resume_id):
    return Resume.query.filter(
        and_(Resume.id == resume_id, Resume.user_id == current_user.id)
    ).first_or_404()


# ==========================================
# Upload Resume
# ==========================================

@resume_bp.route(
    "/upload-resume",
    methods=["GET", "POST"]
)
@login_required
def upload_resume():

    if request.method == "POST":

        if "resume" not in request.files:

            flash("No File Selected")
            return redirect(request.url)

        file = request.files["resume"]

        if file.filename == "":

            flash("Please Select a File")
            return redirect(request.url)

        if file and allowed_file(
            file.filename
        ):

            os.makedirs(
                current_app.config[
                    "UPLOAD_FOLDER"
                ],
                exist_ok=True
            )

            filename = secure_filename(
                file.filename
            )

            filepath = os.path.join(
                current_app.config[
                    "UPLOAD_FOLDER"
                ],
                filename
            )

            file.save(filepath)

            resume = Resume(
                user_id=current_user.id,
                file_name=filename,
                file_path=filepath
            )

            db.session.add(
                resume
            )

            db.session.commit()

            flash(
                "Resume Uploaded Successfully"
            )

            return redirect(
                "/resume-history"
            )

    return render_template(
        "upload_resume.html"
    )


# ==========================================
# Resume History
# ==========================================

@resume_bp.route(
    "/resume-history"
)
@login_required
def resume_history():

    resumes = Resume.query.filter_by(
        user_id=current_user.id
    ).order_by(Resume.id.desc()).all()

    return render_template(
        "resume_history.html",
        resumes=resumes
    )


# ==========================================
# Download Resume
# ==========================================

@resume_bp.route(
    "/download/<filename>"
)
@login_required
def download_resume(filename):

    return send_from_directory(
        current_app.config[
            "UPLOAD_FOLDER"
        ],
        filename,
        as_attachment=True
    )


# ==========================================
# Resume Parser
# ==========================================

@resume_bp.route(
    "/parse-resume/<int:id>"
)
@login_required
def parse_resume(id):

    resume = _get_user_resume(id)

    parser = ResumeParser(
        resume.file_path
    )

    result = parser.parse()

    return render_template(
        "parsed_resume.html",
        result=result
    )


# ==========================================
# ATS Analyzer
# ==========================================

@resume_bp.route(
    "/ats-analyzer/<int:id>"
)
@login_required
def ats_analyzer(id):

    resume = _get_user_resume(id)

    parser = ResumeParser(
        resume.file_path
    )

    parsed_data = parser.parse()

    analyzer = ATSAnalyzer(
        parsed_data
    )

    report = analyzer.analyze()
    resume.ats_score = report.get("score", report.get("ats_score", 0))
    db.session.commit()

    return render_template(
        "ats_report.html",
        report=report
    )


# ==========================================
# Resume vs Job Description Matching
# ==========================================

@resume_bp.route(
    "/match-job/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def match_job(id):

    resume = _get_user_resume(id)

    if request.method == "POST":

        job_description = request.form.get(
            "job_description"
        )

        parser = ResumeParser(
            resume.file_path
        )

        matcher = JDMatcher(
            parser.text,
            job_description
        )

        report = matcher.analyze()

        return render_template(
            "jd_match_report.html",
            report=report
        )

    return render_template(
        "jd_match_form.html"
    )


# ==========================================
# Career Prediction
# ==========================================

@resume_bp.route(
    "/career-prediction/<int:id>"
)
@login_required
def career_prediction(id):

    resume = _get_user_resume(id)

    parser = ResumeParser(
        resume.file_path
    )

    parsed_data = parser.parse()

    predictor = CareerPredictor()

    result = predictor.predict(
        parsed_data["skills"]
    )

    return render_template(
        "career_prediction.html",
        result=result
    )
    
from services.skill_gap_service import (
    SkillGapAnalyzer
)

# ==========================================
# Skill Gap Analysis
# ==========================================

@resume_bp.route(
    "/skill-gap/<int:id>"
)
@login_required
def skill_gap(id):

    resume = _get_user_resume(id)

    parser = ResumeParser(
        resume.file_path
    )

    parsed_data = parser.parse()

    analyzer = SkillGapAnalyzer(

        parsed_data["skills"],

        "AI Engineer"
    )

    report = analyzer.analyze()

    return render_template(
        "skill_gap_report.html",
        report=report
    )
# ==========================================
# Learning Roadmap
# ==========================================
from services.roadmap_service import (
    RoadmapGenerator
)
@resume_bp.route(
    "/roadmap/<int:id>"
)
@login_required
def roadmap(id):

    resume = _get_user_resume(id)

    parser = ResumeParser(
        resume.file_path
    )

    parsed_data = parser.parse()

    analyzer = SkillGapAnalyzer(
        parsed_data["skills"],
        "AI Engineer"
    )

    report = analyzer.analyze()

    generator = RoadmapGenerator(
        report["missing_skills"]
    )

    roadmap = generator.generate()

    return render_template(
        "roadmap.html",
        roadmap=roadmap
    )
# ==========================================
# Interview Question Generator
# ==========================================
from services.interview_service import (
    InterviewGenerator
)
@resume_bp.route(
    "/interview/<int:id>"
)
@login_required
def interview_questions(id):

    resume = _get_user_resume(id)

    parser = ResumeParser(
        resume.file_path
    )

    parsed_data = parser.parse()

    generator = InterviewGenerator(
        parsed_data["skills"]
    )

    questions = generator.generate()

    return render_template(
        "interview_questions.html",
        questions=questions
    )

# ==========================================
# Resume Improvement Suggestions
# ==========================================

from services.resume_improvement_service import (
    ResumeImprovementService
)

@resume_bp.route(
    "/resume-improvement/<int:id>"
)
@login_required
def resume_improvement(id):

    resume = _get_user_resume(id)

    parser = ResumeParser(
        resume.file_path
    )

    parsed_data = parser.parse()

    service = ResumeImprovementService(
        parsed_data
    )

    suggestions = service.analyze()

    return render_template(
        "resume_improvement.html",
        suggestions=suggestions
    )

# ==========================================
# Dashboard Analytics
# ==========================================

from services.dashboard_service import (
    DashboardService
)

@resume_bp.route(
    "/dashboard-analytics/<int:id>"
)
@login_required
def dashboard_analytics(id):

    resume = _get_user_resume(id)

    parser = ResumeParser(
        resume.file_path
    )

    parsed_data = parser.parse()

    service = DashboardService(
        parsed_data
    )

    report = service.generate()

    return render_template(
        "dashboard_analytics.html",
        report=report
    )

# ==========================================
# PDF Report Export 
# ==========================================

from services.pdf_service import (
    PDFReportGenerator
)

@resume_bp.route(
    "/pdf-report/<int:id>"
)
@login_required
def pdf_report(id):

    resume = _get_user_resume(id)

    parser = ResumeParser(
        resume.file_path
    )

    parsed_data = parser.parse()

    report_data = {

        "Skills":
        ", ".join(
            parsed_data["skills"]
        ),

        "Projects":
        len(
            parsed_data["projects"]
        ),

        "Experience":
        len(
            parsed_data["experience"]
        ),

        "Education":
        len(
            parsed_data["education"]
        )
    }

    filename = (
        f"report_{id}.pdf"
    )

    generator = PDFReportGenerator(
        filename,
        report_data
    )

    generator.generate()

    return send_from_directory(
        ".",
        filename,
        as_attachment=True
    )