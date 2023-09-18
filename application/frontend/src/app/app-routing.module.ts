import { NgModule } from '@angular/core'
import { RouterModule, Routes } from '@angular/router'
import { ChatNewComponent } from './chat-new/chat-new.component'
import { TestComponent } from './test/test.component'

const routes: Routes = [
  {
    path: '',
    component: ChatNewComponent,
  },
  {
    path: 'test',
    component: TestComponent,
  },
]

@NgModule({
  imports: [RouterModule.forRoot(routes, { useHash: true })],
  exports: [RouterModule],
})
export class AppRoutingModule {}
