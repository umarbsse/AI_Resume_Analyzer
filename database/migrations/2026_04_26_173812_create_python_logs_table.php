<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('python_logs', function (Blueprint $table) {
            $table->id();
            $table->unsignedBigInteger('resume_id')->nullable();
            $table->string('level', 20);
            $table->text('message');
            $table->timestamps();

            $table->index('resume_id');
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('python_logs');
    }
};