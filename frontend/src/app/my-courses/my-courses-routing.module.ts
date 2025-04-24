/**
 * The My Courses Routing Module holds all of the routes that are children
 * to the path /my-courses/...
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MyCoursesPageComponent } from './my-courses-page/my-courses-page.component';
import { CatalogComponent } from './catalog/catalog.component';
import { AllCoursesComponent } from './catalog/course-catalog/course-catalog.component';
import { SectionOfferingsComponent } from './catalog/section-offerings/section-offerings.component';
import { CourseComponent } from './course/course.component';
import { RosterComponent } from './course/roster/roster.component';
import { PracticeComponent } from './course/practice/practice.component';
import { OfficeHoursPageComponent } from './course/office-hours/office-hours-page/office-hours-page.component';
import { OfficeHoursQueueComponent } from './course/office-hours/office-hours-queue/office-hours-queue.component';
import { OfficeHoursGetHelpComponent } from './course/office-hours/office-hours-get-help/office-hours-get-help.component';
import { SettingsComponent } from './course/settings/settings.component';
import { OfficeHoursEditorComponent } from './course/office-hours/office-hours-editor/office-hours-editor.component';
import { GenerateTestComponent } from './course/practice/generate-test/generate-test.component';

import { GenerateTestResultComponent } from './course/practice/generate-test/result/generate-test-result.component';
import { SelectionComponent } from './course/practice/generate-test/selection/selection.component';
import { InputComponent } from './course/practice/generate-test/input/input.component';
import { UploadComponent } from './course/practice/upload/upload.component';
import { ViewResourcesComponent } from './course/practice/upload/view-resources/view-resources.component';

const routes: Routes = [
  MyCoursesPageComponent.Route,
  {
    path: 'catalog',
    component: CatalogComponent,
    children: [AllCoursesComponent.Route, SectionOfferingsComponent.Route]
  },
  {
    path: 'course/:course_site_id',
    component: CourseComponent,
    children: [
      RosterComponent.Route,
      SettingsComponent.Route,
      OfficeHoursPageComponent.Route,
      OfficeHoursQueueComponent.Route,
      OfficeHoursGetHelpComponent.Route,
      OfficeHoursEditorComponent.Route,
      {
        path: 'practice',
        component: PracticeComponent
      },
      {
        path: 'practice/generate',
        component: GenerateTestComponent,
        children: [
          {
            path: '',
            redirectTo: 'selection',
            pathMatch: 'full'
          },
          {
            path: 'selection',
            component: SelectionComponent
          },
          {
            path: 'input',
            component: InputComponent
          },
          {
            path: 'result/:id',
            component: GenerateTestResultComponent
          }
        ]
      },
      {
        path: 'practice/upload',
        component: UploadComponent,
        children: [
          {
            path: 'view-resources',
            component: ViewResourcesComponent
          }
        ]
      }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class MyCoursesRoutingModule {}
