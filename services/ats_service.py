from nlp.skills_db import SKILLS


class ATSAnalyzer:

    def __init__(self, parsed_resume):

        self.parsed_resume = parsed_resume

    def calculate_score(self):

        found_skills = self.parsed_resume[
            "skills"
        ]

        score = int(
            (
                len(found_skills)
                /
                len(SKILLS)
            ) * 100
        )

        return min(score, 100)

    def missing_keywords(self):

        found = set(
            skill.lower()
            for skill in self.parsed_resume[
                "skills"
            ]
        )

        missing = []

        for skill in SKILLS:

            if skill.lower() not in found:

                missing.append(skill)

        return missing[:10]

    def suggestions(self):

        suggestions = []

        score = self.calculate_score()

        if score < 40:

            suggestions.append(
                "Add more technical skills."
            )

        if len(
            self.parsed_resume[
                "projects"
            ]
        ) == 0:

            suggestions.append(
                "Add project experience."
            )

        if len(
            self.parsed_resume[
                "experience"
            ]
        ) == 0:

            suggestions.append(
                "Add internship or work experience."
            )

        if len(
            self.parsed_resume[
                "education"
            ]
        ) == 0:

            suggestions.append(
                "Add education details."
            )

        if not suggestions:

            suggestions.append(
                "Resume looks ATS friendly."
            )

        return suggestions

    def analyze(self):

        return {

            "score":
            self.calculate_score(),

            "missing_keywords":
            self.missing_keywords(),

            "suggestions":
            self.suggestions()
        }
