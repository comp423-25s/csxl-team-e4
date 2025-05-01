import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { MatListModule } from '@angular/material/list';

@Component({
  selector: 'app-generate-test-result',
  standalone: true,
  imports: [CommonModule, MatCardModule, MatButtonModule, MatListModule],
  templateUrl: './generate-test-result.component.html',
  styleUrl: './generate-test-result.component.css',
  host: {
    class: 'generate-test-container'
  }
})
export class GenerateTestResultComponent implements OnInit {
  testData: any = null;
  isLoading = true;
  downloadUrl: string | null = null;
  resourceId!: string;

  constructor(
    private route: ActivatedRoute,
    private http: HttpClient
  ) {}

  ngOnInit() {
    this.resourceId = this.route.snapshot.paramMap.get('id')!;
    this.http
      .get(`/api/academics/practice_test/retrieve_response/${this.resourceId}`)
      .subscribe({
        next: (data) => {
          this.testData = data;
          this.isLoading = false;
          this.loadPdfPreview();
        },
        error: () => {
          alert('Failed to load test result.');
          this.isLoading = false;
        }
      });
  }

  loadPdfPreview() {
    this.http
      .get(`/api/academics/practice_test/generate_pdf/${this.resourceId}`, {
        responseType: 'blob'
      })
      .subscribe({
        next: (blob) => {
          const pdfUrl = URL.createObjectURL(blob);
          this.downloadUrl = pdfUrl;

          const iframe = document.getElementById(
            'pdf-preview'
          ) as HTMLIFrameElement;
          if (iframe) {
            iframe.src = pdfUrl;
          }
        },
        error: () => {
          alert('Failed to generate PDF');
        }
      });
  }
}
