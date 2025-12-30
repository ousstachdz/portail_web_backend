// Define ManagementTeamTable Component
class ManagementTeamTable extends Component {
  static props = ['state']

  setup() {
    this.deleteManager = this.deleteManager.bind(this)
  }

  static template = xml`
    <div class="tableWrapper">
      <table  class="table table-striped table-responsive">
        <thead class="fw-bold">
          <tr>
          <th>السيد(ة)</th>
          <th>المهنة</th>
          <th>المستوى الدراسي</th>
          <th>السن</th>
          <th>الخبرة المهنية</th>
          <th></th>
        </tr>
      </thead>
      <tbody id="gestion">
        <t t-foreach="props.state.managers" t-as="manager" t-key="manager.id">
          <tr>
            <td><span><t t-esc="manager.name"/></span></td>
            <td><span><t t-esc="manager.job"/></span></td>
            <td><span><t t-esc="manager.niveau_etude"/></span></td>
            <td><span><t t-esc="manager.age"/></span></td>
            <td><span><t t-esc="manager.experience"/></span></td>
            <td>
              <button type="button" class="btn btn-danger" t-on-click="(e) => deleteManager(manager.id, e)">حذف</button>
            </td>
          </tr>
        </t>
      </tbody>
    </table>
    </div>
  `

  deleteManager(id, e) {
    e.preventDefault()
    console.log('Delete Manager with ID:', id)
    const state = this.props.state
    if (state) {
      state.managers = state.managers.filter((manager) => manager.id !== id)
    } else {
      console.error('State is not accessible in ManagementTeamTable')
    }
  }
}

// Define AddManagementTeam Component
class AddManagementTeam extends Component {
  static props = ['state']

  setup() {
    this.state = useState({
      name: '',
      job: '',
      niveau_etude: '',
      age: '',
      experience: '',
    })
  }

  handleSubmit(event) {
    event.preventDefault()
    const newManager = {
      id: Date.now(), // Generate a unique ID
      name: this.state.name,
      job: this.state.job,
      niveau_etude: this.state.niveau_etude,
      age: this.state.age,
      experience: this.state.experience,
    }
    const { state } = this.props
    if (state) {
      state.managers.push(newManager)
    } else {
      console.error('State is not accessible in AddManagementTeam')
    }
    // Reset form fields
    this.state.name = ''
    this.state.job = ''
    this.state.niveau_etude = ''
    this.state.age = ''
    this.state.experience = ''
  }

  static template = xml`
    <div class="modal fade" id="createGestionModal" tabindex="-1" aria-labelledby="createGestionModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
                             <div class="modal-header d-flex justify-content-between align-items-center">


            <h5 class="modal-title" id="createGestionModalLabel">اضف مسير</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form t-on-submit="handleSubmit" style="padding: 10px">
              <div class="mb-3">
                <label for="name">السيد(ة)</label>
                <input type="text" t-model="state.name" class="form-control form-control-sm" id="name" name="name" required="required"/>
              </div>
              <div class="mb-3">
                <label for="job">المهنة</label>
                <input type="text" t-model="state.job" class="form-control form-control-sm" id="job" name="job" required="required"/>
              </div>
              <div class="mb-3">
                <label for="niveau_etude">المستوى الدراسي</label>
                <input type="text" t-model="state.niveau_etude" class="form-control form-control-sm" id="niveau_etude" name="niveau_etude" required="required"/>
              </div>
              <div class="mb-3">
                <label for="age">السن</label>
                <input type="number" t-model="state.age" class="form-control form-control-sm" id="age" name="age"/>
              </div>
              <div class="mb-3">
                <label for="experience">الخبرة المهنية</label>
                <input type="number" t-model="state.experience" class="form-control form-control-sm" id="experience" name="experience"/>
              </div>
              <button type="submit" class="btn btn-secondary">اضف</button>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          </div>
        </div>
      </div>
    </div>
  `
}

// Define Index Component
class ManagementTeam extends Component {
  static props = ['state']

  static components = {
    ManagementTeamTable,
    AddManagementTeam,
  }

  static template = xml`
    <div>
      <AddManagementTeam state="props.state"/>
      <ManagementTeamTable state="props.state"/>
    </div>
  `
}
