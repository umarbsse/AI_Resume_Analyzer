import re
from db import get_connection


# =====================================================
# ANALYZE RESUME VS JOB DESCRIPTION
# =====================================================

def analyze_resume_text(resume_text, job_description):

    # -----------------------------------------------------
    # SAFE CLEANING
    # -----------------------------------------------------
    resume_text = (resume_text or "").strip()
    job_description = (job_description or "").strip()

    if resume_text == "" or job_description == "":
        return {
            "match_score": 0,
            "strengths": "Resume or job description missing in analysis input",
            "improvements": "Ensure resume_text and job_description are stored in DB",
            "suggestions": "Check DB data insertion flow"
        }

    # -----------------------------------------------------
    # LOWERCASE
    # -----------------------------------------------------
    resume_text_lower = resume_text.lower()
    job_text_lower = job_description.lower()

    # -----------------------------------------------------
    # STEP 1: GET ALL TECH KEYWORDS
    # -----------------------------------------------------
    tech_keywords = get_tech_keywords()
    tech_keywords_set = set([kw.lower() for kw in tech_keywords])

    # -----------------------------------------------------
    # STEP 2: EXTRACT KEYWORDS FROM JOB DESCRIPTION
    # -----------------------------------------------------
    job_words = set(re.findall(r'\b[a-zA-Z]{3,}\b', job_text_lower))

    # Only keep TECH-related keywords from job description
    job_keywords = [kw for kw in job_words if kw in tech_keywords_set]

    # -----------------------------------------------------
    # STEP 3: FIND MATCHED + MISSING IN RESUME
    # -----------------------------------------------------
    matched_keywords = [kw for kw in job_keywords if kw in resume_text_lower]
    missing_keywords = [kw for kw in job_keywords if kw not in resume_text_lower]

    # -----------------------------------------------------
    # STEP 4: MATCH SCORE
    # -----------------------------------------------------
    if len(job_keywords) == 0:
        match_score = 0
    else:
        match_score = int((len(matched_keywords) / len(job_keywords)) * 100)

    # -----------------------------------------------------
    # STEP 5: INSIGHTS
    # -----------------------------------------------------
    strengths = []
    improvements = []
    suggestions = []

    # Strengths
    if match_score >= 70:
        strengths.append("Strong match with job description")
    elif match_score >= 40:
        strengths.append("Moderate match with job description")
    else:
        improvements.append("Low keyword match with job description")

    # Add matched skills
    if matched_keywords:
        strengths.append("Matched skills: " + ", ".join(matched_keywords[:10]))

    # Missing skills
    if missing_keywords:
        improvements.append("Missing skills: " + ", ".join(missing_keywords[:10]))

    # Resume quality checks
    if "project" not in resume_text_lower:
        improvements.append("Add project experience section")

    if len(resume_text.split()) < 200:
        improvements.append("Resume content is too short")

    # Suggestions
    if match_score < 50:
        suggestions.append("Improve keyword alignment with job description")

    if match_score < 70:
        suggestions.append("Customize resume based on job requirements")

    if missing_keywords:
        suggestions.append("Add missing skills if you have experience")

    if not strengths:
        strengths.append("Basic resume structure detected")

    # -----------------------------------------------------
    # FINAL RETURN
    # -----------------------------------------------------
    return {
        "match_score": match_score,
        "strengths": ", ".join(strengths),
        "improvements": ", ".join(improvements),
        "suggestions": ", ".join(suggestions)
    }


# =====================================================
# Keywords to look for in job descriptions and resumes
# =====================================================
def get_tech_keywords():
    return [

                    # -----------------------------
                    # Programming Languages
                    # -----------------------------
                    "python","java","javascript","typescript","c","c++","c#","go","golang","rust",
                    "kotlin","swift","dart","ruby","php","scala","perl","r","matlab","haskell",
                    "objective-c","elixir","clojure","groovy","f#","assembly","bash","powershell",

                    # -----------------------------
                    # Backend Frameworks
                    # -----------------------------
                    "django","flask","fastapi","spring","spring boot","micronaut","quarkus",
                    "express","nestjs","koa","hapi","asp.net","asp.net core","laravel",
                    "symfony","codeigniter","adonisjs","sails","phoenix",

                    # -----------------------------
                    # Frontend Frameworks / UI
                    # -----------------------------
                    "react","nextjs","vue","nuxt","angular","svelte","ember","backbone",
                    "jquery","redux","zustand","mobx","vite","webpack","babel",
                    "html","html5","css","css3","sass","scss","less","bootstrap","tailwind",
                    "material ui","chakra ui","ant design",

                    # -----------------------------
                    # Mobile / Cross Platform
                    # -----------------------------
                    "android","ios","react native","flutter","xamarin","ionic","swiftui",
                    "jetpack compose","cordova","capacitor",

                    # -----------------------------
                    # Databases (SQL/NoSQL)
                    # -----------------------------
                    "mysql","postgresql","postgres","sqlite","mariadb","oracle","sql server",
                    "mongodb","cassandra","dynamodb","redis","memcached","neo4j",
                    "elasticsearch","opensearch","firebase","supabase","cockroachdb","timescaledb",

                    # -----------------------------
                    # Cloud / DevOps
                    # -----------------------------
                    "aws","amazon web services","azure","gcp","google cloud","digitalocean",
                    "linode","heroku","vercel","netlify",
                    "docker","kubernetes","helm","openshift","nomad",
                    "terraform","pulumi","ansible","chef","puppet",
                    "jenkins","github actions","gitlab ci","circleci","travis ci",
                    "nginx","apache","caddy",

                    # -----------------------------
                    # Data / AI / ML
                    # -----------------------------
                    "machine learning","deep learning","ai","artificial intelligence",
                    "tensorflow","pytorch","keras","scikit-learn","xgboost","lightgbm",
                    "pandas","numpy","matplotlib","seaborn","opencv","nlp","spacy",
                    "huggingface","transformers","llm","gpt","bert",
                    "data analysis","data science","data engineering",
                    "spark","apache spark","hadoop","hive","airflow","dbt",

                    # -----------------------------
                    # APIs & Integration
                    # -----------------------------
                    "rest","rest api","graphql","grpc","soap","websocket",
                    "openapi","swagger","postman","insomnia",

                    # -----------------------------
                    # Testing
                    # -----------------------------
                    "unit testing","integration testing","e2e testing","tdd","bdd",
                    "selenium","cypress","playwright","jest","mocha","chai",
                    "junit","pytest","phpunit","karma","vitest",

                    # -----------------------------
                    # Version Control / Collaboration
                    # -----------------------------
                    "git","github","gitlab","bitbucket","svn",

                    # -----------------------------
                    # Security
                    # -----------------------------
                    "oauth","oauth2","jwt","saml","openid","encryption","ssl","tls",
                    "owasp","xss","csrf","sql injection","penetration testing","pentesting",
                    "security","cybersecurity","iam","zero trust",

                    # -----------------------------
                    # Architecture / Patterns
                    # -----------------------------
                    "microservices","monolith","event driven","soa","mvc","mvvm",
                    "clean architecture","hexagonal architecture","ddd","cqrs",
                    "design patterns","singleton","factory","observer",

                    # -----------------------------
                    # Messaging / Streaming
                    # -----------------------------
                    "kafka","rabbitmq","activemq","nats","redis streams","pubsub",

                    # -----------------------------
                    # Containers / Orchestration
                    # -----------------------------
                    "containerization","docker compose","kubernetes","k8s","helm charts",

                    # -----------------------------
                    # Operating Systems / Infra
                    # -----------------------------
                    "linux","ubuntu","debian","centos","windows","macos","unix",

                    # -----------------------------
                    # Build / Package Managers
                    # -----------------------------
                    "npm","yarn","pnpm","pip","poetry","maven","gradle","composer","nuget",

                    # -----------------------------
                    # CMS / E-commerce
                    # -----------------------------
                    "wordpress","drupal","joomla","shopify","magento","woocommerce",

                    # -----------------------------
                    # Analytics / Monitoring
                    # -----------------------------
                    "prometheus","grafana","elk","elastic stack","logstash","kibana",
                    "datadog","new relic","sentry",

                    # -----------------------------
                    # Misc / Productivity
                    # -----------------------------
                    "jira","confluence","agile","scrum","kanban","ci/cd","devops",
                    "debugging","optimization","performance tuning"
        ]



# =====================================================
# UPDATE DB
# =====================================================
def update_analysis(resume_id, analysis):

    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            UPDATE resume_analyzer
            SET match_score=%s,
                strengths=%s,
                improvements_needed=%s,
                suggestions=%s,
                updated_at=NOW()
            WHERE id=%s
        """

        cursor.execute(query, (
            analysis["match_score"],
            analysis["strengths"],
            analysis["improvements"],
            analysis["suggestions"],
            resume_id
        ))

        conn.commit()
        conn.close()

        print(f"Analysis updated for resume ID: {resume_id}")

    except Exception as e:
        print("DB update error:", str(e))