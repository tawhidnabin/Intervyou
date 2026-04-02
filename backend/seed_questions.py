"""
IntervYou Question Bank — 60+ questions across 4 categories and 3 difficulty levels.
Categories: general, behavioural, motivational, technical
"""

QUESTIONS = [
    # ═══════════════════════════════════════════════════════════════
    # BEGINNER (easy)
    # ═══════════════════════════════════════════════════════════════

    # General — easy
    ('Tell me about yourself.', 'general', 'easy', 'I am a motivated professional with experience in my field. I have developed strong skills through education and practical work. I am passionate about continuous learning and contributing to team success.'),
    ('What are your greatest strengths?', 'general', 'easy', 'My greatest strengths are problem-solving, communication, and adaptability. I approach challenges methodically and work well in teams.'),
    ('What is your biggest weakness?', 'general', 'easy', 'I sometimes take on too much work because I want to ensure quality. I have been actively working on delegating tasks and trusting my team.'),
    ('Why should we hire you?', 'general', 'easy', 'You should hire me because I bring relevant skills, enthusiasm, and a strong work ethic. I am a quick learner committed to delivering high-quality results.'),
    ('How would your friends describe you?', 'general', 'easy', 'My friends would describe me as reliable, thoughtful, and someone who follows through on commitments. I am known for being a good listener and offering practical advice.'),
    ('What do you know about our company?', 'general', 'easy', 'I have researched your company and I am impressed by your mission, recent growth, and commitment to innovation. Your values align with my professional goals.'),
    ('What are your salary expectations?', 'general', 'easy', 'Based on my research and experience level, I am looking for a salary in the range typical for this role in this market. I am open to discussing the full compensation package.'),

    # Behavioural — easy
    ('Tell me about a time you worked in a team.', 'behavioural', 'easy', 'In a previous project I collaborated with a cross-functional team to deliver a product launch. I coordinated communication between departments, ensuring alignment on goals and deadlines.'),
    ('Describe a time you helped someone.', 'behavioural', 'easy', 'A colleague was struggling with a deadline so I offered to review their work and help prioritise tasks. Together we completed the project on time and they thanked me for the support.'),
    ('Tell me about a time you made a mistake at work.', 'behavioural', 'easy', 'I once sent a report with incorrect data. I immediately notified my manager, corrected the error, and implemented a double-check process to prevent it happening again.'),
    ('Describe a time you received positive feedback.', 'behavioural', 'easy', 'After leading a successful client presentation, my manager praised my preparation and clear communication. This reinforced my belief in thorough preparation.'),

    # Motivational — easy
    ('Why do you want this job?', 'motivational', 'easy', 'I am excited about this role because it aligns with my skills and career goals. The company mission resonates with me and I believe I can make a meaningful contribution.'),
    ('Where do you see yourself in 5 years?', 'motivational', 'easy', 'In five years I see myself having grown within this organisation, taking on greater responsibilities and contributing to strategic decisions.'),
    ('What motivates you?', 'motivational', 'easy', 'I am motivated by solving meaningful problems, learning new skills, and seeing the impact of my work. Working with talented people who push me to grow also drives me.'),
    ('Why are you leaving your current job?', 'motivational', 'easy', 'I am looking for new challenges and opportunities to grow. While I value my current experience, this role offers the next step in my career development.'),
    ('What are your career goals?', 'motivational', 'easy', 'My goal is to develop deep expertise in my field while growing into a leadership role where I can mentor others and drive impactful projects.'),

    # Technical — easy
    ('What programming languages do you know?', 'technical', 'easy', 'I am proficient in Python and JavaScript, with working knowledge of Java and SQL. I choose the right language based on the project requirements.'),
    ('Explain what an API is.', 'technical', 'easy', 'An API is an Application Programming Interface — it defines how different software systems communicate with each other. For example, a REST API uses HTTP requests to send and receive data in JSON format.'),
    ('What is version control and why is it important?', 'technical', 'easy', 'Version control like Git tracks changes to code over time, allows multiple developers to collaborate, and provides the ability to revert to previous versions if something breaks.'),
    ('What is the difference between frontend and backend?', 'technical', 'easy', 'Frontend is what users see and interact with in the browser — HTML, CSS, JavaScript. Backend is the server-side logic, database, and APIs that power the application behind the scenes.'),

    # ═══════════════════════════════════════════════════════════════
    # INTERMEDIATE (medium)
    # ═══════════════════════════════════════════════════════════════

    # General — medium
    ('How do you prioritise when you have multiple deadlines?', 'general', 'medium', 'I use urgency and impact to prioritise. I list all tasks, assess deadlines and business value, then tackle high-impact urgent items first. I communicate proactively if any deadlines are at risk.'),
    ('How do you handle feedback and criticism?', 'general', 'medium', 'I welcome feedback as an opportunity to grow. I listen without becoming defensive, ask clarifying questions, and create an action plan to address it.'),
    ('Describe your ideal work environment.', 'general', 'medium', 'I thrive in collaborative environments with clear goals, open communication, and autonomy to make decisions. I value a culture that encourages learning and supports work-life balance.'),
    ('How do you stay current with industry trends?', 'general', 'medium', 'I follow industry blogs, attend webinars, participate in online communities, and dedicate time each week to learning new tools and techniques relevant to my field.'),
    ('What would you do in your first 90 days?', 'general', 'medium', 'In the first 30 days I would learn the systems, meet the team, and understand current priorities. By day 60 I would start contributing to projects. By day 90 I would aim to deliver measurable value.'),

    # Behavioural — medium
    ('Describe a challenge you overcame.', 'behavioural', 'medium', 'A project deadline was moved forward unexpectedly. I prioritised tasks, communicated with stakeholders, delegated effectively, and delivered on time. It taught me resilience and time management.'),
    ('Tell me about a time you showed leadership.', 'behavioural', 'medium', 'When our team lead was absent during a critical sprint, I coordinated standups, unblocked team members, and communicated progress to stakeholders. The sprint was delivered on time.'),
    ('How do you handle conflict with a colleague?', 'behavioural', 'medium', 'I address conflict directly but respectfully by seeking to understand the other perspective. I arrange a private conversation, listen actively, and focus on finding a solution.'),
    ('Describe a time you failed and what you learned.', 'behavioural', 'medium', 'I underestimated a feature\'s complexity and missed a deadline. I took ownership, communicated transparently, created a recovery plan, and learned to break down tasks more carefully.'),
    ('Tell me about a time you had to learn something quickly.', 'behavioural', 'medium', 'When we adopted a new tech stack mid-project, I dedicated evenings to learning, built prototypes, and paired with experienced colleagues. Within two weeks I was contributing effectively.'),
    ('Describe a time you went above and beyond.', 'behavioural', 'medium', 'A client needed an urgent fix over a weekend. I volunteered to work through Saturday, resolved the issue, and documented the solution. The client renewed their contract as a result.'),
    ('Tell me about a time you had to persuade someone.', 'behavioural', 'medium', 'I needed to convince my team to adopt automated testing. I ran a pilot, showed the time savings with data, and addressed their concerns. The team adopted it within a month.'),

    # Motivational — medium
    ('What do you find most rewarding about your work?', 'motivational', 'medium', 'I find it most rewarding when I solve a complex problem that has real impact. Seeing users benefit from something I built gives me a strong sense of purpose.'),
    ('How do you handle stress and pressure?', 'motivational', 'medium', 'I break large problems into smaller tasks, prioritise ruthlessly, and take short breaks to maintain focus. I also communicate early if I foresee any risks to deadlines.'),
    ('What would make you leave a job?', 'motivational', 'medium', 'I would leave if there were no opportunities for growth, if the culture became toxic, or if the work no longer aligned with my values and career goals.'),

    # Technical — medium
    ('Explain the difference between SQL and NoSQL databases.', 'technical', 'medium', 'SQL databases are relational with structured schemas and support complex joins. NoSQL databases are flexible, schema-less, and better for unstructured data and horizontal scaling.'),
    ('What is RESTful API design?', 'technical', 'medium', 'REST uses HTTP methods (GET, POST, PUT, DELETE) to perform CRUD operations on resources identified by URLs. It is stateless, meaning each request contains all information needed to process it.'),
    ('How do you approach debugging a production issue?', 'technical', 'medium', 'I start by reproducing the issue, check logs and monitoring dashboards, isolate the component, form a hypothesis, test it, deploy a fix, and then conduct a post-mortem.'),
    ('What is CI/CD and why is it important?', 'technical', 'medium', 'CI/CD automates building, testing, and deploying code. Continuous Integration catches bugs early by running tests on every commit. Continuous Deployment automates releases, reducing manual errors.'),
    ('Explain how authentication with JWT works.', 'technical', 'medium', 'The user logs in with credentials, the server verifies them and returns a signed JWT token. The client sends this token in the Authorization header with each request. The server validates the signature without needing to store session state.'),

    # ═══════════════════════════════════════════════════════════════
    # MASTER (hard)
    # ═══════════════════════════════════════════════════════════════

    # General — hard
    ('How do you approach making decisions with incomplete information?', 'general', 'hard', 'I identify the minimum viable information needed, gather it quickly through research and stakeholder input, assess the risk of being wrong, make a time-boxed decision, and build in checkpoints to course-correct.'),
    ('How do you balance technical debt against feature delivery?', 'general', 'hard', 'I treat technical debt as a first-class concern by making it visible with quantified impact. I advocate for 20% of sprint capacity for debt reduction and frame it in business terms.'),
    ('How do you build and maintain high-performing teams?', 'general', 'hard', 'I focus on psychological safety, clear goals, and individual growth. I run regular one-on-ones, celebrate wins publicly, and address underperformance privately and constructively.'),
    ('How do you measure the success of a project?', 'general', 'hard', 'I define success metrics upfront aligned with business objectives — user adoption, revenue impact, system reliability. I track leading indicators during development and lagging indicators post-launch.'),
    ('What is your approach to stakeholder management?', 'general', 'hard', 'I identify all stakeholders early, understand their priorities and concerns, establish regular communication cadences, and proactively manage expectations with transparent progress updates.'),

    # Behavioural — hard
    ('Describe a situation where you influenced a decision without direct authority.', 'behavioural', 'hard', 'I identified a process inefficiency, gathered data to quantify the impact, built a business case, and presented it to senior stakeholders. I secured buy-in and led the implementation, reducing processing time by 40%.'),
    ('Tell me about the most complex problem you have solved.', 'behavioural', 'hard', 'I diagnosed a production system degradation affecting thousands of users. I isolated variables, analysed logs, identified a race condition, and coordinated a hotfix within four hours. I then led a post-mortem.'),
    ('Describe a time you drove significant change in an organisation.', 'behavioural', 'hard', 'I championed a shift from waterfall to agile. I piloted with one team, measured improvements, built a case for wider adoption, ran training sessions, and the methodology was adopted across three teams.'),
    ('Tell me about a time you had to deliver difficult news to a stakeholder.', 'behavioural', 'hard', 'I informed a key client that a feature would be delayed by three weeks. I presented the situation transparently with root cause analysis, offered mitigation options, and recommended the best path forward.'),
    ('Describe a time you had to make an unpopular decision.', 'behavioural', 'hard', 'I decided to cancel a feature that the team had spent weeks on because user research showed it would not deliver value. I presented the data, acknowledged the team\'s effort, and redirected resources to higher-impact work.'),
    ('Tell me about a time you managed a crisis.', 'behavioural', 'hard', 'During a major outage I coordinated the incident response, assigned roles, communicated with affected customers, and led the technical investigation. We restored service within two hours and I led the post-incident review.'),

    # Motivational — hard
    ('What is your leadership philosophy?', 'motivational', 'hard', 'I believe in servant leadership — removing blockers, providing context, and empowering people to make decisions. I set clear expectations, give autonomy, and hold people accountable for outcomes, not process.'),
    ('How do you handle disagreements with your manager?', 'motivational', 'hard', 'I present my perspective with data and reasoning, listen to their viewpoint, and seek to understand the broader context I might be missing. If we still disagree, I commit to the decision and execute fully.'),
    ('What legacy do you want to leave at a company?', 'motivational', 'hard', 'I want to be remembered for building systems and teams that thrive after I leave. I focus on documentation, mentoring, and creating processes that scale beyond any individual.'),

    # Technical — hard
    ('How would you design a system to handle 10 million users?', 'technical', 'hard', 'I would use a microservices architecture with horizontal scaling, a CDN for static assets, database sharding or read replicas, caching layers like Redis, message queues for async processing, and auto-scaling groups behind a load balancer.'),
    ('Explain the CAP theorem and its practical implications.', 'technical', 'hard', 'The CAP theorem states that a distributed system can only guarantee two of three: Consistency, Availability, and Partition tolerance. In practice, since network partitions are inevitable, you choose between consistency and availability based on your use case.'),
    ('How do you approach system security in a web application?', 'technical', 'hard', 'I implement defence in depth: input validation, parameterised queries, JWT with short expiry, HTTPS everywhere, CORS restrictions, rate limiting, dependency scanning, and regular security audits. I follow OWASP Top 10 guidelines.'),
    ('What is your approach to monitoring and observability?', 'technical', 'hard', 'I implement the three pillars: metrics (Prometheus/Grafana), logs (structured JSON, centralised), and traces (distributed tracing). I set up alerts on SLOs and create dashboards for key business and technical metrics.'),
]
