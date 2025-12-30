const { Component, useState, mount, xml } = owl

class AproposTable extends Component {
  static props = ['state']

  setup() {
    this.deletePartner = this.deletePartner.bind(this)
  }

  static template = xml`
    <div class="tableWrapper">
      <table  class="table table-striped table-responsive">
        <thead class="fw-bold">
          <tr>
            <th>اسم الشريك/المالك</th>
            <th>الجنسية</th>
            <th>تاريخ التاسيس/الميلاد</th>
            <th>نسبة الحصة</th>
            <th>صفة الشريك</th>
            <th>حذف</th>
          </tr>  
        </thead>
        <tbody class="">
            <t t-foreach="props.state.partners" t-as="partner" t-key="partner.id">
              <tr>
                <td><t t-esc="partner.nom_partenaire"/></td>
                <td><span><t t-esc="partner.countryName"/></span></td>
                <td><t t-esc="partner.age"/></td>
                <td><t t-esc="partner.pourcentage"/></td>
                <td><t t-esc="partner.statut_partenaire"/></td>
                <td>
                  <button type="button" class="btn btn-danger" t-on-click="(e) => 
                      deletePartner(partner.id,e)
                      ">حذف</button>
                </td>
              </tr>
            </t>
        </tbody>
      </table>
    </div>
  `
  deletePartner(id, e) {
    e.preventDefault()
    console.log('Delete Partner with ID:', id)
    const state = this.props.state
    if (state) {
      state.partners = state.partners.filter((partner) => partner.id !== id)
    } else {
      console.error('State is not accessible in AproposTable')
    }
  }
}

class AddPartner extends Component {
  static props = ['state']

  setup() {
    this.state = useState({
      nom_partenaire: '',
      country: '',
      countryName: '',
      age: '',
      pourcentage: '',
      statut_partenaire: '',
    })
  }

  handleSubmit(event) {
    event.preventDefault()
    const newPartner = {
      id: Date.now(), // Generate a unique ID
      nom_partenaire: this.state.nom_partenaire,
      country: this.state.country,
      countryName: this.state.countryName,
      age: this.state.age,
      pourcentage: this.state.pourcentage,
      statut_partenaire: this.state.statut_partenaire,
    }
    const { state } = this.props
    if (state) {
      state.partners.push(newPartner)
    } else {
      console.error('State is not accessible in AddPartner')
    }
    // Reset form fields
    this.state.nom_partenaire = ''
    this.state.country = ''
    this.state.countryName = ''
    this.state.age = ''
    this.state.pourcentage = ''
    this.state.statut_partenaire = ''
  }

  handleCountryChange(event) {
    const countryId = event.target.value
    const countryName = event.target.options[event.target.selectedIndex].text

    this.state.country = countryId
    this.state.countryName = countryName
  }

  static template = xml`
    <div class="modal fade" id="createAproposModal" tabindex="-1" aria-labelledby="createAproposModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
                    <div class="modal-header d-flex justify-content-between align-items-center">

                    <h5 class="modal-title" id="createAproposModalLabel">اضف شريك</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <form t-on-submit="handleSubmit">
          <div class="modal-body"  style="padding: 10px" >
              <div class="mb-3">
                <label for="nom_partenaire">اسم الشريك/المالك</label>
                <input type="text" t-model="state.nom_partenaire" class="form-control form-control-sm" id="nom_partenaire" name="partner_name" required="required"/>
              </div>
              <div class="mb-3">
                <label for="age">تاريخ التاسيس/الميلاد</label>
                <input type="date" t-model="state.age" class="form-control form-control-sm" id="age" name="partner_age" required="required"/>
              </div>
              <div class="mb-3">
                <label for="pourcentage">نسبة الحصة</label>
                <input type="number" t-model="state.pourcentage" class="form-control form-control-sm" id="pourcentage" name="partner_prrcentage" required="required"/>
              </div>
              <div class="mb-3">
                <label for="statut_partenaire">صفة الشريك</label>
                <input type="text" t-model="state.statut_partenaire" class="form-control form-control-sm" id="statut_partenaire" name="partner_status"/>
              </div>

               <div class="mb-3">
                <label for="country">الجنسية</label>
                <select t-model="state.country" name="country" id="country" class="form-control link-style" t-on-change="handleCountryChange">
                  <option value="" disabled="1" selected="1" >اختر الجنسية</option>  
                <t t-foreach="props.state.data.nationalites" t-as="country" t-key='country.id'>
                    <option t-att-value="country.id">
                      <t t-esc="country.name"/>
                    </option>
                  </t>
                </select>
              </div>

              </div>
              <div class="modal-footer">
              <button type="submit" class="btn btn-secondary"  data-bs-dismiss="modal">اضف</button>
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
              </div>
              </form>
        </div>
      </div>
    </div>
  `
}

// Define Index Component
class Partners extends Component {
  static props = ['state']

  static components = {
    AproposTable,
    AddPartner,
  }

  static template = xml`
    <div>
      <AddPartner state="props.state"/>
      <AproposTable state="props.state"/>
    </div>
  `
}
