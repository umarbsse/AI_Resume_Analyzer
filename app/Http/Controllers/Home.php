<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class Home extends Controller
{
    // Add this function:
    public function index()
    {
         // Create an array of data
        $data = [
            'project_name' => 'AI Resume Analyzer',
            'version' => '1.0.2',
            'features' => ['PDF Parsing', 'Skill Extraction', 'Score Generation']
        ];
        return view('bootstrap.home',$data); 
    }
}
