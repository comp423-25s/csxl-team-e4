import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-generate-test-result',
  standalone: true,
  imports: [CommonModule, MatCardModule, MatButtonModule],
  templateUrl: './generate-test-result.component.html',
  styleUrl: './generate-test-result.component.css',
  host: {
    class: 'generate-test-container'
  }
})
export class GenerateTestResultComponent implements OnInit {
  testData: any = null;
  isLoading = true;

  constructor(
    private route: ActivatedRoute,
    private http: HttpClient
  ) {}

  ngOnInit() {
    const id = this.route.snapshot.paramMap.get('id');
    this.http
      .get(`/api/academics/practice_test/retrieve_response/${id}`)
      .subscribe({
        next: (data) => {
          this.testData = data;
          this.isLoading = false;
        },
        error: () => {
          alert('Failed to load test result.');
          this.isLoading = false;
        }
      });
  }
}
