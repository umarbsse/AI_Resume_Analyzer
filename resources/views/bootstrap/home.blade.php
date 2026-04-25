<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Resume Analyzer</title>

    <!-- Bootstrap 5 CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>

<body class="bg-light">

<div class="container py-5">
    
    <!-- Header -->
    <div class="text-center mb-5">
        <h1 class="fw-bold">AI Resume Analyzer</h1>
        <p class="text-muted">Upload your resume and match it with a job description</p>
    </div>

    <!-- Main Card -->
    <div class="card shadow-lg border-0">
        <div class="card-body p-4">
@if ($errors->any())
    <div class="alert alert-danger">
        <ul>
            @foreach ($errors->all() as $error)
                <li>{{ $error }}</li>
            @endforeach
        </ul>
    </div>
@endif

@if(session('success'))
    <div class="alert alert-success">{{ session('success') }}</div>
@endif

        <form action="{{ route('analyze_resume') }}" method="POST" enctype="multipart/form-data">
        @csrf 

    <!-- Resume Upload -->
    <div class="mb-4">
        <label class="form-label fw-semibold">Upload Resume</label>
        <!-- ADDED name="resume" -->
        <input type="file" name="resume" class="form-control" accept=".pdf">
    </div>

    <!-- Job Description -->
    <div class="mb-4">
        <label class="form-label fw-semibold">Paste Job Description</label>
        <!-- ADDED name="job_description" -->
        <textarea name="job_description" class="form-control" rows="6" placeholder="Paste job description here..."></textarea>
    </div>

    <!-- Button -->
    <div class="text-center">
        <button type="submit" class="btn btn-primary px-5 py-2">Analyze Resume</button>
    </div>
</form>


        </div>
    </div>

    <!-- Results Section -->
    <div class="mt-5">
        <div class="card border-0 shadow">
            <div class="card-body p-4">

                <h4 class="mb-3">Analysis Result</h4>

                <!-- Score -->
                <div class="mb-4">
                    <h5>Match Score</h5>
                    <div class="progress">
                        <div class="progress-bar bg-success" style="width: 75%;">75%</div>
                    </div>
                </div>

                <!-- Strengths -->
                <div class="mb-3">
                    <h5 class="text-success">Strengths</h5>
                    <ul>
                        <li>Good experience with React and Node.js</li>
                        <li>Strong backend development skills</li>
                        <li>Relevant database experience</li>
                    </ul>
                </div>

                <!-- Weaknesses -->
                <div class="mb-3">
                    <h5 class="text-danger">Improvements Needed</h5>
                    <ul>
                        <li>Add more DevOps experience</li>
                        <li>Include cloud technologies (AWS/Azure)</li>
                        <li>Improve keyword matching for ATS</li>
                    </ul>
                </div>

                <!-- Suggestions -->
                <div>
                    <h5 class="text-primary">Suggestions</h5>
                    <ul>
                        <li>Include measurable achievements</li>
                        <li>Use more job-specific keywords</li>
                        <li>Optimize resume summary section</li>
                    </ul>
                </div>

            </div>
        </div>
    </div>

</div>

</body>
</html>