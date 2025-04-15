import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';
import { SharedModule } from 'src/app/shared/shared.module';
import {
  Router,
  ActivatedRoute,
  RouterModule,
  NavigationEnd
} from '@angular/router';
import { MatDivider } from '@angular/material/divider';
import { ReactiveFormsModule } from '@angular/forms';
import { FormArray, FormControl } from '@angular/forms';
import { PracticeTestService } from '../../../../../services/practice-test.service';
import { PracticeTestFormService } from '../../../../../services/practice-test-form.service';

@Component({
  selector: 'app-generate-input',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    RouterModule,
    MatDivider,
    SharedModule,
    CommonModule,
    FormsModule,
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule,
    MatCardModule,
    MatIconModule
  ],
  templateUrl: './input.component.html',
  styleUrl: './input.component.css'
})
export class InputComponent {
  readonly isResultPage = signal(false);

  testFormatOptions = [
    'Multiple Choice',
    'Short Answer',
    'Free Response',
    'Code Writing'
  ];
  form = this.practiceTestFormService.getForm();
  formats = this.practiceTestFormService.formats;

  toggleFormat(format: string) {
    this.practiceTestFormService.toggleFormat(format);
  }

  get formatsArray(): FormArray {
    return this.form.get('formats') as FormArray;
  }

  formatSelected(option: string): boolean {
    return this.formatsArray.value.includes(option);
  }

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private practiceTestService: PracticeTestService,
    private practiceTestFormService: PracticeTestFormService
  ) {
    this.router.events.subscribe((event) => {
      if (event instanceof NavigationEnd) {
        this.isResultPage.set(this.router.url.endsWith('/result'));
      }
    });
  }

  goBack() {
    this.router.navigate(['../'], { relativeTo: this.route });
  }

  goForward() {
    this.router.navigate(['../result'], { relativeTo: this.route });
  }

  generateNewTest() {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }
    const payload = this.form.value;
    this.practiceTestService.generateTest(payload).subscribe({
      next: (res) => {
        this.practiceTestFormService.resetForm();
        this.router.navigate(['../result'], { relativeTo: this.route });
      },
      error: () => alert('Failed to generate test.')
    });
  }

  get promptControl() {
    return this.form.get('prompt') as FormControl;
  }
}
