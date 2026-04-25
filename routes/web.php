<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Home;
use App\Http\Controllers\Ai;



Route::get('/', [Home::class, 'index']);



// Change the route to point to analyze_resume
Route::post('/analyze_resume', [Ai::class, 'analyze_resume'])->name('analyze_resume');