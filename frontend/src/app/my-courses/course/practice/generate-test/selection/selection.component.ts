import { Component, effect, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatListModule } from '@angular/material/list';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatCardModule } from '@angular/material/card';
import { SharedModule } from 'src/app/shared/shared.module';
import { FormArray, FormBuilder } from '@angular/forms';
import { PracticeTestFormService } from '../../../../../services/practice-test-form.service';
import { FormsModule } from '@angular/forms';
import { ResourceService, Resource } from 'src/app/services/resource.service';

import {
  ActivatedRoute,
  NavigationEnd,
  Router,
  RouterModule
} from '@angular/router';
import { Profile, ProfileService } from 'src/app/profile/profile.service';
import { Observable } from 'rxjs';
import { PermissionService } from 'src/app/permission.service';

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
    MatCardModule
  ],
  templateUrl: './selection.component.html',
  styleUrl: './selection.component.css'
})
export class SelectionComponent {
  public adminPermission$: Observable<boolean>;
  profile?: Profile | undefined;
  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private practiceTestFormService: PracticeTestFormService,
    protected permission: PermissionService,
    private resourceService: ResourceService,
    private fb: FormBuilder,
    private profileService: ProfileService
  ) {
    this.profileService.profile$.subscribe((profile) => {
      this.profile = profile ?? undefined;
    });
    this.adminPermission$ = this.permission.check('admin.view', 'admin/');
    const course_id = this.route.snapshot.params['course_site_id'];
    this.resourceService.getResources(course_id).subscribe({
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

  get resource_ids(): FormArray {
    return this.form.get('resource_ids') as FormArray;
  }

  isSelected(id: number): boolean {
    return this.resource_ids?.value?.includes(id) ?? false;
  }

  toggleSelect(id: number) {
    const ids = this.form.get('resource_ids') as FormArray;
    const index = ids.value.indexOf(id);
    if (index === -1) {
      ids.push(this.fb.control(id));
    } else {
      ids.removeAt(index);
    }
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
    if (item.ta_upload && this.profile && this.profile.last_name == 'Student') {
      alert("You're not allowed to delete TA materials.");
    } else {
      this.resourceService.deleteResource(item.id).subscribe({
        next: () => {
          this.resources.set(this.resources().filter((r) => r.id !== item.id));
        },
        error: () => alert('Delete failed.')
      });
    }
  }

  goToInputPage() {
    this.router.navigate(['../input'], { relativeTo: this.route });
  }
}
