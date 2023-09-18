import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { ReactiveFormsModule } from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FormsModule } from '@angular/forms';
import { MatRadioModule } from '@angular/material/radio';
import { MatButtonModule } from '@angular/material/button';
import { HttpClientModule } from '@angular/common/http';
import { MatIconModule } from '@angular/material/icon';
import { AppService } from './app.service';
import { ChatNewComponent } from './chat-new/chat-new.component';
import { TestComponent } from './test/test.component';

@NgModule({
  declarations: [AppComponent, ChatNewComponent, TestComponent],

  imports: [
    BrowserModule,
    HttpClientModule,
    FormsModule,
    MatRadioModule,
    MatButtonModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatIconModule,
  ],
  providers: [AppService],
  bootstrap: [AppComponent],
})
export class AppModule {}
