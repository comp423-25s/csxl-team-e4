import { Component, effect, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatListModule } from '@angular/material/list';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatCardModule } from '@angular/material/card';
import { SharedModule } from 'src/app/shared/shared.module';
import { FormArray, FormControl } from '@angular/forms'; 
import { PracticeTestService } from '../../../../../services/practice-test.service';
import { PracticeTestFormService } from '../../../../../services/practice-test-form.service';
import { FormsModule } from '@angular/forms';
import { 
  ActivatedRoute,
  NavigationEnd,
  Router,
  RouterModule,
} from '@angular/router';

@Component({
  selector: 'app-selection',
  standalone: true,
  imports: [
    RouterModule,
    SharedModule,
    CommonModule,
    FormsModule,
    MatListModule,
    MatIconModule,
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule,
    MatCardModule],
  templateUrl: './selection.component.html',
  styleUrl: './selection.component.css'
})
export class SelectionComponent {
  constructor(
      private router: Router,
      private route: ActivatedRoute,
      private practiceTestService: PracticeTestService,
      private practiceTestFormService: PracticeTestFormService
  
    ) {
      effect(() => {
        const url = this.router.url;
        this.isResultPage.set(url.endsWith('/result'));
      });
  
      this.router.events.subscribe((event) => {
        if (event instanceof NavigationEnd) {
          this.isResultPage.set(this.router.url.endsWith('/result'));
        }
      });
    }

    form = this.practiceTestFormService.getForm();

    get materialArray(): FormArray {
      return this.form.get('material') as FormArray;
    }
    
    toggleSelect(id: number) {
      const materials = this.materialArray;
      const index = materials.value.indexOf(id);
      if (index === -1) {
        materials.push(new FormControl(id));
      } else {
        materials.removeAt(index);
      }
    }
    
    isSelected(id: number): boolean {
      return this.materialArray?.value?.includes(id) ?? false;
    }
    
  materials: { id: number; title: string }[] = [
    { id: 1, title: 'Study Guide Unit 2 Topic 3' },
    { id: 2, title: 'Study Guide Unit 2 Topic 4' },
    { id: 3, title: 'Study Guide Unit 2 Topic 1' },
    { id: 4, title: 'Study Guide Unit 2 Topic 2' },
    { id: 5, title: 'Study Guide Unit 2 Topic 5' },
    { id: 6, title: 'Study Guide Unit 2 Topic 6' },
    { id: 7, title: 'Study Guide Unit 2 Topic 7' },
    { id: 8, title: 'Study Guide Unit 2 Topic 8' },
    { id: 9, title: 'Study Guide Unit 2 Topic 9' }
  ];

  readonly isResultPage = signal(false);

  goToResultPage() {
    this.router.navigate(['result'], { relativeTo: this.route });
  }

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
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }
    // model of data to be sent to the backend
    const payload = this.form.value;

    this.practiceTestService.generateTest(payload).subscribe({
      next: (res) => {
        const generatedId = res.response_id;
        this.practiceTestFormService.resetForm();
        this.router.navigate(['/my-courses/course/practice/generate-test/result', generatedId]);
      },
      error: () => alert('Failed to generate test.')
    });
  }

  goToInputPage() {
    this.router.navigate(['../input'], { relativeTo: this.route });
  }
}