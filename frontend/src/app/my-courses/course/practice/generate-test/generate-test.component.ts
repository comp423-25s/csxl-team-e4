import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { SharedModule } from 'src/app/shared/shared.module';


@Component({
  selector: 'app-generate-test',
  standalone: true,

  imports: [RouterOutlet, SharedModule],
  templateUrl: './generate-test.component.html',
  styleUrl: './generate-test.component.css'
})
export class GenerateTestComponent {}
