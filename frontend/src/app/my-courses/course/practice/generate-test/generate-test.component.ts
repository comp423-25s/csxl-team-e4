import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatListModule } from '@angular/material/list';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { SharedModule } from 'src/app/shared/shared.module';
import { PracticeTestService } from '../../../../services/practice-test.service';
import { Router } from '@angular/router';




@Component({
  selector: 'app-generate-test',
  standalone: true,
  imports: [
    SharedModule,
    CommonModule,
    FormsModule,
    MatListModule,
    MatIconModule,
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule,
    MatCardModule
  ],
  templateUrl: './generate-test.component.html',
  styleUrl: './generate-test.component.css'
})




export class GenerateTestComponent {
  materials: { id: number; title: string }[] = [
    { id: 1, title: 'Study Guide Unit 2 Topic 3' },
    { id: 2, title: 'Study Guide Unit 2 Topic 4' },
    { id: 3, title: 'Study Guide Unit 2 Topic 1' }
  ];
  
  inputText = '';

  constructor(
    private practiceTestService: PracticeTestService,
    private router: Router
  ) {}

  downloadMaterial(item: any) {
    this.practiceTestService.getTest(item.id).subscribe({
      next: (res) => {
        console.log('Downloaded:', res);
        alert(`Downloaded "${item.title}"`);
      },
      error: () => alert('Download failed.')
    });
  }

  deleteMaterial(item: any) {
    this.practiceTestService.deleteTest(item.id).subscribe({
      next: () => {
        this.materials = this.materials.filter(m => m.id !== item.id);
      },
      error: () => alert('Delete failed.')
    });
  }

  generateNewTest() {
    this.practiceTestService.generateTest(this.inputText).subscribe({
      next: (res) => {
        const generatedId = res.response_id;
        this.inputText = '';
  
        // 👇 Route to the page your partner made
        this.router.navigate(['/my-courses/practice/view', generatedId]);
      },
      error: () => alert('Failed to generate test.')
    });
  }
}

