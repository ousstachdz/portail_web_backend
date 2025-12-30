// Define FinancialRequestsTable Component
class FinancialRequestsTable extends Component {
  static props = ['state']

  setup() {
    this.deleteRequest = this.deleteRequest.bind(this)
  }

  deleteRequest(id, e) {
    e.preventDefault()
    console.log('Delete Request with ID:', id)
    const state = this.props.state
    if (state) {
      state.tailles = state.tailles.filter((taille) => taille.id !== id)
    } else {
      console.error('State is not accessible in FinancialRequestsTable')
    }
  }

  static template = xml`
    <div class="tableWrapper">
      <table  class="table table-striped table-responsive">
        <thead class="fw-bold">
          <tr>
          <th>نوع التسهيلات</th>
          <th>المبلغ المطلوب</th>
          <th>الغرض من التمويل</th>
          <th>الضمانات المقترحة</th>
          <th>هامش الجدية</th>
          <th>المدة (الايام)</th>
          <th>حذف</th>
        </tr>
      </thead>
      <tbody id="financial_request">
        <t t-foreach="props.state.tailles" t-as="taille" t-key="taille.id">
          <tr>
            <td><span><t t-esc="taille.type_demande.name"/></span></td>
            <td><span><t t-esc="taille.montant"/></span></td>
            <td><span><t t-esc="taille.raison"/></span></td>
            <td>
              <span>
                <ul>
                  <t t-foreach="taille.garantiesNames" t-as="garantieName" t-key="garantieName">
                    <li>-   <t t-esc="garantieName"/></li>
                  </t>
                </ul>
              </span>
            </td>
            <td><span><t t-esc="taille.preg"/></span></td>
            <td><span><t t-esc="taille.duree"/></span></td>
            <td>
              <button type="button" class="btn btn-danger" t-on-click="(e) => deleteRequest(taille.id, e)">حذف</button>
            </td>
          </tr>
        </t>
      </tbody>
    </table>
    </div>
  `
}
class AddFinancialRequest extends Component {
  static props = ['state']

  setup() {
    this.state = useState({
      type_demande: '',
      type_demande_name: '', // Store type_demande name
      montant: '',
      raison: '',
      garanties: [], // Initialize as an empty array
      garantiesNames: [], // Initialize as an empty array
      preg: '',
      duree: '',
    })
  }

  handleSubmit(event) {
    event.preventDefault()

    const newRequest = {
      id: Date.now(),
      type_demande: { name: this.state.type_demande_name }, // Store name as well
      montant: this.state.montant,
      raison: this.state.raison,
      garanties: this.state.garanties, // Save guarantee IDs
      garantiesNames: this.state.garantiesNames, // Save guarantee names
      preg: this.state.preg,
      duree: this.state.duree,
    }
    const { state } = this.props
    if (state) {
      state.tailles.push(newRequest)
    } else {
      console.error('State is not accessible in AddFinancialRequest')
    }
    // Reset form fields
    this.state.type_demande = ''
    this.state.type_demande_name = ''
    this.state.montant = ''
    this.state.raison = ''
    this.state.garanties = []
    this.state.garantiesNames = []
    this.state.preg = ''
    this.state.duree = ''

    // Uncheck all checkboxes after submission
    document.querySelectorAll('.form-check-input').forEach((checkbox) => {
      checkbox.checked = false
    })
  }

  handleGuaranteeChange(event) {
    const guaranteeId = event.target.getAttribute('data-guarantee-id')
    const guaranteeName = event.target.getAttribute('data-guarantee-name')
    const isChecked = event.target.checked

    if (isChecked) {
      this.state.garanties.push(guaranteeId) // Add guarantee ID
      this.state.garantiesNames.push(guaranteeName) // Add guarantee name
    } else {
      const idIndex = this.state.garanties.indexOf(guaranteeId)
      if (idIndex !== -1) {
        this.state.garanties.splice(idIndex, 1) // Remove guarantee ID
      }

      const nameIndex = this.state.garantiesNames.indexOf(guaranteeName)
      if (nameIndex !== -1) {
        this.state.garantiesNames.splice(nameIndex, 1) // Remove guarantee name
      }
    }
  }

  handleTypeDemandeChange(event) {
    const typeDemandeId = event.target.value
    const typeDemandeName =
      event.target.options[event.target.selectedIndex].text

    this.state.type_demande = typeDemandeId
    this.state.type_demande_name = typeDemandeName
  }

  static template = xml`
    <div class="modal fade" id="createRequestModal" tabindex="-1" aria-labelledby="createRequestModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
                             <div class="modal-header d-flex justify-content-between align-items-center">


            <h5 class="modal-title" id="createRequestModalLabel">اضف طلب</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form t-on-submit="handleSubmit" style="padding: 10px">
              <div class="mb-3">
                <label for="type_demande">نوع التسهيلات</label>
                <select t-model="state.type_demande" name="type_demande" id="type_demande" class="form-control link-style" t-on-change="handleTypeDemandeChange">
                  <option value="" disabled="1" selected="1" >اختر نوع التسهيلات</option>  
                <t t-foreach="props.state.data.type_demande_ids" t-as="type_demande" t-key="type_demande.id">
                    <option t-att-value="type_demande.id">
                      <t t-esc="type_demande.name"/>
                    </option>
                  </t>
                </select>
              </div>
              <div class="mb-3">
                <label for="montant">المبلغ المطلوب</label>
                <input type="number" t-model="state.montant" class="form-control form-control-sm" id="montant" name="montant" required="required"/>
              </div>
              <div class="mb-3">
                <label for="raison">الغرض من التمويل</label>
                <input type="text" t-model="state.raison" class="form-control form-control-sm" id="raison" name="raison" required="required"/>
              </div>
              <div class="mb-3">
                <label for="garanties">الضمانات المقترحة</label>
                <t t-foreach="props.state.data.garanties_ids" t-as="garantie" t-key="garantie.id">
                  <div class="form-check">
                    <input type="checkbox" class="form-check-input"
                          t-att-id="'garantie_' + garantie.id"
                          t-att-name="'garantie_' + garantie.id"
                          t-att-value="garantie.id"
                          t-att-data-guarantee-id="garantie.id"
                          t-att-data-guarantee-name="garantie.name"
                          t-on-change="handleGuaranteeChange"/>
                    <label class="form-check-label" t-att-for="'garantie_' + garantie.id">
                      <t t-esc="garantie.name"/>
                    </label>
                  </div>
                </t>
              </div>
              <div class="mb-3">
                <label for="preg">هامش الجدية</label>
                <input type="number" t-model="state.preg" class="form-control form-control-sm" id="preg" name="preg"/>
              </div>
              <div class="mb-3">
                <label for="duree">المدة (الايام)</label>
                <input type="number" t-model="state.duree" class="form-control form-control-sm" id="duree" name="duree"/>
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

class FinancialRequestIndex extends Component {
  static props = ['state']

  static components = {
    FinancialRequestsTable,
    AddFinancialRequest,
  }

  static template = xml`
    <div>
      <AddFinancialRequest state="props.state"/>
      <FinancialRequestsTable state="props.state"/>
    </div>
  `
}
