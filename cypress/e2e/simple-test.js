describe('Full stack e2e', () => {
  it('Query tool', () => {
    cy.visit('http://localhost:3000/')
    cy.get('[data-cy="Neurobagel graph-categorical-field"]').type(
      'local graph 1{downarrow}{enter}'
    );
    cy.get('[data-cy="submit-query-button"]').click();
    cy.get('[data-cy="result-container"]').contains("from Local graph 1",{matchCase: false});
  })
  it('API', () => {
    cy.request("localhost:8000/query/").as("query");
    cy.get("@query").should((response) => {
      expect(response.status).to.eq(200);
    });
  });
  it("Federation API", () => {
    cy.request("localhost:8000/query/?node=local graph 1").as("query");
    cy.get("@query").should((response) => {
      expect(response.status).to.eq(200);
    });
  })
  it("CLI", () => {
    cy.exec("docker run --rm neurobagel/bagelcli --help").its("stdout").should("contain", "Usage: bagel");
  });
})
