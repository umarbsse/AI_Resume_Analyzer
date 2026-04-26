<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('resume_analyzer', function (Blueprint $table) {
            $table->id();
            $table->string('file_path');
            $table->string('original_filename');
            $table->text('resume_text')->nullable();
            $table->text('job_description');
            
            // AI Feedback Fields
            $table->text('strengths')->nullable();           // List of what the candidate did well
            $table->text('improvements_needed')->nullable(); // Areas lacking in the resume
            $table->text('suggestions')->nullable();         // Actionable advice for the candidate
            
            $table->integer('match_score')->nullable();
            $table->timestamps();   
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('resume_analyzer');
    }
};
