// Define AddSituation Component
class AddSituation extends Component {
  static props = ['state']

  setup() {
    this.state = useState({
      banqueId: '',
      banqueName: '',
      typeFinId: '',
      typeFinName: '',
      situationMontant: '',
      situationEncours: '',
      situationGaranties: [],
    })
  }

  handleSubmit(event) {
    event.preventDefault()
    const newSituationRequest = {
      id: Date.now(), // Generate a unique ID
      banque: { id: this.state.banqueId, name: this.state.banqueName },
      typeFin: { id: this.state.typeFinId, name: this.state.typeFinName },
      situationMontant: this.state.situationMontant,
      situationEncours: this.state.situationEncours,
      situationGaranties: this.state.situationGaranties
        .split(',')
        .map((name) => ({ name: name.trim() })),
    }

    const { state } = this.props
    if (state) {
      state.situationTailles.push(newSituationRequest)
    } else {
      console.error('State is not accessible in AddSituation')
    }

    // Reset form fields after submission
    this.state.banqueId = ''
    this.state.banqueName = ''
    this.state.typeFinId = ''
    this.state.typeFinName = ''
    this.state.situationMontant = ''
    this.state.situationEncours = ''
    this.state.situationGaranties = ''
  }

  handleBanqueChange(event) {
    const selectedOption = event.target.options[event.target.selectedIndex]
    this.state.banqueId = event.target.value
    this.state.banqueName = selectedOption.text
  }

  handleTypeFinChange(event) {
    const selectedOption = event.target.options[event.target.selectedIndex]
    this.state.typeFinId = event.target.value
    this.state.typeFinName = selectedOption.text
  }

  static template = xml`
    <div class="modal fade" id="createSituationModal" tabindex="-1" aria-labelledby="createSituationModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
                             <div class="modal-header d-flex justify-content-between align-items-center">


            <h5 class="modal-title" id="createSituationModalLabel">اضف طلب</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form t-on-submit="handleSubmit" style="padding: 10px">
              <div class="mb-3">
                <label for="banque">البنك</label>
                <select name="banque" id="banque" class="form-control link-style" t-on-change="handleBanqueChange">
                  <option value="" disabled="1" selected="1" >اختر البنك</option> 
                <t t-foreach="props.state.data.banque_ids" t-as="banque" t-key="banque.id">
                    <option t-att-value="banque.id">
                      <t t-esc="banque.name"/>
                    </option>
                  </t>
                </select>
              </div>
              <div class="mb-3">
                <label for="type_fin">نوع التمويل</label>
                <select name="type_fin" id="type_fin" class="form-control link-style" t-on-change="handleTypeFinChange">
                  <option value="" disabled="1" selected="1" >اختر نوع التمويل</option>  
                <t t-foreach="props.state.data.type_fin_ids" t-as="type_fin" t-key="type_fin.id">
                    <option t-att-value="type_fin.id">
                      <t t-esc="type_fin.name"/>
                    </option>
                  </t>
                </select>
              </div>
              <div class="mb-3">
                <label for="situationMontant">المبلغ KDA</label>
                <input type="number" t-model="this.state.situationMontant" id="situationMontant" name="situationMontant" required="required" class="form-control form-control-sm"/>
              </div>
              <div class="mb-3">
                <label for="situationEncours">المبلغ المستغل KDA</label>
                <input type="number" t-model="this.state.situationEncours" id="situationEncours" name="situationEncours" required="required" class="form-control form-control-sm"/>
              </div>
              <div class="mb-3">
                <label for="situationGaranties">الضمانات الممنوحة</label>
                <input type="text" t-model="this.state.situationGaranties" id="situationGaranties" name="situationGaranties" class="form-control form-control-sm"/>
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

// Define SituationTable Component
class SituationTable extends Component {
  static props = ['state']

  setup() {
    this.deleteSituationRequest = this.deleteSituationRequest.bind(this)
  }

  deleteSituationRequest(id, e) {
    e.preventDefault()
    const { state } = this.props
    if (state) {
      state.situationTailles = state.situationTailles.filter(
        (situation) => situation.id !== id
      )
    } else {
      console.error('State is not accessible in SituationTable')
    }
  }

  static template = xml`
     <div class="tableWrapper">
      <table  class="table table-striped table-responsive">
        <thead class="fw-bold">
          <tr>
          <th>البنك</th>
          <th>نوع التمويل</th>
          <th>المبلغ KDA</th>
          <th>المبلغ المستغل KDA</th>
          <th>الضمانات الممنوحة</th>
                    <th>حذف</th>

        </tr>
      </thead>
      <tbody id="situation">
        <t t-foreach="props.state.situationTailles" t-as="situation" t-key="situation.id">
          <tr>
            <td><span><t t-esc="situation.banque.name"/></span></td>
            <td><span><t t-esc="situation.typeFin.name"/></span></td>
            <td><span><t t-esc="situation.situationMontant"/></span></td>
            <td><span><t t-esc="situation.situationEncours"/></span></td>
            <td><span><t t-esc="situation.situationGaranties.map(g => g.name).join(', ')"/></span></td>
            <td>
              <button t-on-click="(e) => deleteSituationRequest(situation.id, e)" class="btn btn-danger">Delete</button>
            </td>
          </tr>
        </t>
      </tbody>
    </table>
    </div>
  `
}
// Define SituationIndex Component
class SituationIndex extends Component {
  static props = ['state']

  static components = {
    SituationTable,
    AddSituation,
  }

  static template = xml`
    <div>
      <AddSituation state="props.state"/>
      <SituationTable state="props.state"/>
    </div>
  `
}
