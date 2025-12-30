class CompaniesTable extends Component {
  static props = ['state']

  setup() {
    this.deleteCompanies = this.deleteCompanies.bind(this)
  }

  static template = xml`
    <div class="tableWrapper">
      <table  class="table table-striped table-responsive">
        <thead class="fw-bold">
          <tr>
              <th>الشركة</th>
              <th>سنة التاسيس</th>
              <th>النشاط الرئيسي</th>
              <th>راس المال</th>
              <th>رقم الاعمال N-1</th>
              <th>رقم الاعمال N</th>
              <th>حذف</th>
            </tr>
          </thead>
          <tbody id="company">
            <t t-foreach="props.state.companies" t-as="company" t-key="company.id">
              <tr>
                <td>
                  <span>
                    <t t-esc="company.name"/>
                  </span>
                </td>
                <td>
                  <span>
                    <t t-esc="company.fond_date"/>
                  </span>
                </td>
                <td>
                  <span>
                    <t t-esc="company.activityName"/>
                  </span>
                </td>
                <td>
                  <span>
                    <t t-esc="company.capital"/>
                  </span>
                </td>
                <td>
                  <span>
                    <t t-esc="company.n1"/>
                  </span>
                </td>
                <td>
                  <span>
                    <t t-esc="company.n"/>
                  </span>
                </td>
                <td>
                  <button type="button" class="btn btn-danger" t-on-click="(e) => deleteCompanies(company.id, e)">حذف</button>
                </td>
              </tr>
            </t>
          </tbody>
        </table>
      </div>
      `

  deleteCompanies(id, e) {
    e.preventDefault()
    console.log('Delete company with ID:', id)
    const state = this.props.state
    if (state) {
      state.companies = state.companies.filter((company) => company.id !== id)
    } else {
      console.error('State is not accessible in CompaniesTable')
    }
  }
}

class AddCompanies extends Component {
  static props = ['state']

  setup() {
    this.state = useState({
      name: '',
      fond_date: '',
      activity: '',
      activityName: '',
      capital: '',
      n1: '',
      n: '',
    })

    this.handleSubmit = this.handleSubmit.bind(this)
    this.handleSelectChange = this.handleSelectChange.bind(this)
  }

  handleSubmit(event) {
    event.preventDefault()
    const newCompany = {
      id: Date.now(), // Generate a unique ID
      name: this.state.name,
      fond_date: this.state.fond_date,
      activity: this.state.activity,
      activityName: this.state.activityName,
      capital: this.state.capital,
      n1: this.state.n1,
      n: this.state.n,
    }
    const { state } = this.props
    if (state) {
      state.companies.push(newCompany)
    } else {
      console.error('State is not accessible in AddCompanies')
    }
    // Reset form fields
    this.state.name = ''
    this.state.fond_date = ''
    this.state.activity = ''
    this.state.activityName = ''
    this.state.capital = ''
    this.state.n1 = ''
    this.state.n = ''
  }

  handleSelectChange(event) {
    const selectedOption = event.target.options[event.target.selectedIndex]
    this.state.activity = event.target.value
    this.state.activityName = selectedOption.text
  }

  static template = xml`
    <div class="modal fade" id="createCompaniesModal" tabindex="-1" aria-labelledby="createCompaniesModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
                             <div class="modal-header d-flex justify-content-between align-items-center">


                   <h5 class="modal-title" id="createCompaniesModalLabel">اضف شركة</h5>
                   <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form t-on-submit="handleSubmit" style="padding: 10px">
              <div class="mb-3">
                <label for="name">الشركة</label>
                <input type="text" t-model="this.state.name" class="form-control form-control-sm" id="name" name="name" required="required"/>
              </div>
              <div class="mb-3">
                <label for="fond_date">سنة التاسيس</label>
                <input type="text" t-model="this.state.fond_date" class="form-control form-control-sm" id="fond_date" name="fond_date" required="required"/>
              </div>
              <div class="mb-3">
                <label for="capital">راس المال</label>
                <input type="text" t-model="this.state.capital" class="form-control form-control-sm" id="capital" name="capital" required="required"/>
              </div>
              <div class="mb-3">
                <label for="n1">رقم الاعمال N-1</label>
                <input type="text" t-model="this.state.n1" class="form-control form-control-sm" id="n1" name="n1" required="required"/>
              </div>
              <div class="mb-3">
                <label for="n">رقم الاعمال N</label>
                <input type="text" t-model="this.state.n" class="form-control form-control-sm" id="n" name="n" required="required"/>
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

// Define CompaniesIndex Component
class CompaniesIndex extends Component {
  static props = ['state']

  static components = {
    CompaniesTable,
    AddCompanies,
  }

  static template = xml`
    <div>
      <AddCompanies state="props.state"/>
      <CompaniesTable state="props.state"/>
    </div>
  `
}
