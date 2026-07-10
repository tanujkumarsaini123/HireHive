def career_advice(cgpa, coding, communication, internships, projects, backlogs):

    advice = []

    if cgpa < 8:
        advice.append("📘 Try to improve your CGPA above 8.0.")

    if coding < 7:
        advice.append("💻 Practice DSA and coding on LeetCode or Codeforces.")

    if communication < 7:
        advice.append("🗣 Improve communication through presentations and mock interviews.")

    if internships == 0:
        advice.append("🏢 Complete at least one internship.")

    if projects < 3:
        advice.append("📂 Build more real-world projects and upload them to GitHub.")

    if backlogs > 0:
        advice.append("❗ Clear all backlogs before placement season.")

    if len(advice) == 0:
        advice.append("🎉 Excellent profile! Keep improving your skills.")

    return advice