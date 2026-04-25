<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Storage;

class Ai extends Controller
{
public function analyze_resume(Request $request)
{
    $request->validate([
        'resume' => 'required|mimes:pdf|max:5120',
        'job_description' => 'required|string',
    ]);

    if ($request->hasFile('resume')) {

        $file = $request->file('resume');

        $destinationPath = base_path('assets/user_upload/resume');

        if (!file_exists($destinationPath)) {
            mkdir($destinationPath, 0777, true);
        }

        $fileName = time() . '_' . $file->getClientOriginalName();
        $file->move($destinationPath, $fileName);

        // Insert DB
        $id = DB::table('resume_analyzer')->insertGetId([
            'file_path' => 'assets/user_upload/resume/' . $fileName,
            'original_filename' => $file->getClientOriginalName(),
            'job_description' => $request->job_description,
            'created_at' => now(),
            'updated_at' => now(),
        ]);

        // Run Python AI
        $python = "C:\Users\John\AppData\Local\Programs\Python\Python314\python.exe";
        $script = base_path('python/analyze_resume.py');
        $command = "$python $script $id";


        

        exec("$python $script $id");

        return back()->with('success', 'Resume uploaded and analyzed!');
    }

    return back()->with('error', 'No file uploaded.');
}
}
