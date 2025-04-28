import { Component, signal, OnInit } from '@angular/core';
import { ActivatedRoute, Router, RouterOutlet } from '@angular/router';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { UploadResourceService } from 'src/app/services/upload-resource.service';
import { AcademicsService } from 'src/app/academics/academics.service';
import { CommonModule } from '@angular/common';
import { SharedModule } from 'src/app/shared/shared.module';
import { MatCardModule } from '@angular/material/card';
import { MatDivider } from '@angular/material/divider';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-upload',
  standalone: true,
  imports: [
    RouterOutlet,
    SharedModule,
    CommonModule,
    ReactiveFormsModule,
    MatCardModule,
    MatDivider,
    MatFormFieldModule,
    MatInputModule,
    MatIconModule,
    RouterModule,
  ],
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.css'],
})
export class UploadComponent implements OnInit {
  uploadForm!: FormGroup;
  selectedFileName = signal('');
  courseId!: string; // 'comp110' or other backend string
  courseSiteId = signal<string | null>(null); // route param like '1'

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private fb: FormBuilder,
    private uploadService: UploadResourceService,
    private academicsService: AcademicsService
  ) {
    this.uploadForm = this.fb.group({
      title: ['', Validators.required],
      file: [null, Validators.required],
    });
  }

  ngOnInit(): void {
    const courseSiteId = this.route.parent?.snapshot.paramMap.get('course_site_id');
    console.log('Resolved course_site_id:', courseSiteId);
  
    if (!courseSiteId) {
      console.error('course_site_id not found');
      return;
    }
  
    this.courseSiteId.set(courseSiteId);
  
    const index = parseInt(courseSiteId);
    this.academicsService.getCourses().subscribe(courses => {
      const matched = courses[index - 1];
      if (matched) {
        this.courseId = matched.id;
        console.log('Resolved courseId for upload:', this.courseId);
      } else {
        console.error('No course found at index', index);
      }
    });
  }

  onFileSelected(event: any) {
    const file = event.target.files[0];
    this.uploadForm.patchValue({ file });
    this.uploadForm.get('file')?.updateValueAndValidity();
  }

  upload() {
    if (this.uploadForm.valid && this.courseId) {
      const title = this.uploadForm.get('title')?.value;
      const file = this.uploadForm.get('file')?.value;
      const fileName = file.name;

      this.uploadService.uploadResource(title, file, fileName, this.courseId).subscribe({
        next: () => alert('Upload successful!'),
        error: (err) => alert('Upload failed: ' + err.message),
      });
    } else {
      alert('Please fill in all required fields.');
    }
  }
}
