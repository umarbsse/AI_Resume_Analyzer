<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Storage;

class Ai extends Controller
{
public function analyze_resume(Request $request)
{
    // 1. Validation
    $request->validate([
        'resume' => 'required|mimes:pdf|max:5120',
        'job_description' => 'required|string',
    ]);

    if ($request->hasFile('resume')) {

        $file = $request->file('resume');

        // Your custom folder path
        $destinationPath = base_path('assets/user_upload/resume');

        // Create folder if not exists
        if (!file_exists($destinationPath)) {
            mkdir($destinationPath, 0777, true);
        }

        // Unique filename
        $fileName = time() . '_' . $file->getClientOriginalName();

        // Move file to your folder
        $file->move($destinationPath, $fileName);

        // Save in DB
        DB::table('resume_analyzer')->insert([
            'file_path' => 'assets/user_upload/resume/' . $fileName,
            'original_filename' => $file->getClientOriginalName(),
            'job_description' => $request->job_description,
            'created_at' => now(),
            'updated_at' => now(),
        ]);

        return back()->with('success', 'Resume uploaded successfully!');
    }

    return back()->with('error', 'No file uploaded.');
}
}
