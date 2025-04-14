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
import { ResourceService, Resource } from 'src/app/services/resource.service';

import { 
  ActivatedRoute,
  NavigationEnd,
  Router,
  RouterModule,
} from '@angular/router';
import { RippleRef } from '@angular/material/core';

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
    private practiceTestFormService: PracticeTestFormService,
    private resourceService: ResourceService
  ) {
    // Simplified — no more dynamic course_id
    this.resourceService.getResources().subscribe({
      next: (res) => this.resources.set(res),
      error: () => alert('Failed to load resources.')
    });

    this.router.events.subscribe((event) => {
      if (event instanceof NavigationEnd) {
        this.isResultPage.set(this.router.url.endsWith('/result'));
      }
    });
  }

  form = this.practiceTestFormService.getForm();
  resources = signal<Resource[]>([]);

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

  readonly isResultPage = signal(false);

  goToResultPage() {
    this.router.navigate(['result'], { relativeTo: this.route });
  }

  downloadMaterial(item: Resource) {
    this.resourceService.downloadResource(item.id).subscribe({
      next: (blob) => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = item.file_name;
        a.click(); // trigger download
        window.URL.revokeObjectURL(url);
      },
      error: () => alert('Download failed.')
    });
  }

  deleteMaterial(item: Resource) {
    this.resourceService.deleteResource(item.id).subscribe({
      next: () => {
        this.resources.set(this.resources().filter(r => r.id !== item.id));
      },
      error: () => alert('Delete failed.')
    });
  }

  generateNewTest() {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

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
