import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GenerateTestResultComponent } from './generate-test-result.component';

describe('GenerateTestResultComponent', () => {
  let component: GenerateTestResultComponent;
  let fixture: ComponentFixture<GenerateTestResultComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GenerateTestResultComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GenerateTestResultComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
