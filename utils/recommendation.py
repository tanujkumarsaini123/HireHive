def recommend_companies(probability, cgpa, coding, internships):

    if probability < 40:
        return [
            "Improve DSA and Coding Skills",
            "Build 3-4 Real Projects",
            "Complete an Internship",
            "Practice Aptitude Daily"
        ]

    elif probability < 70:
        return [
            "Infosys",
            "TCS",
            "Wipro",
            "Capgemini"
        ]

    elif probability < 90:
        return [
            "Accenture",
            "Cognizant",
            "IBM",
            "Deloitte"
        ]

    else:
        return [
            "Google",
            "Microsoft",
            "Amazon",
            "Adobe"
        ]